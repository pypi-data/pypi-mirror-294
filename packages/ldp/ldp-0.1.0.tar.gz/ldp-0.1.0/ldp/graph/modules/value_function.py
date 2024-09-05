from __future__ import annotations

import asyncio
import inspect
import itertools
import json
import random
from abc import abstractmethod
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from copy import deepcopy
from typing import ClassVar, Generic, TypeVar

import torch
import tree
from aviary.message import Message
from aviary.tools import ToolRequestMessage
from torch import nn

from ldp.graph.async_torch import AsyncTorchModule
from ldp.graph.common_ops import FxnOp
from ldp.graph.gradient_estimators import assign_constant_grads
from ldp.graph.op_utils import (
    CallID,
    compute_graph,
    get_call_id,
    get_training_mode,
)
from ldp.graph.ops import GradInType, Op, OpCtx, OpResult, ResultOrValue
from ldp.graph.torch_ops import store_tensor_inputs
from ldp.llms import (
    EmbeddingModel,
    HybridEmbeddingModel,
    LiteEmbeddingModel,
    SparseEmbeddingModel,
)


def get_msg_content(msg: Message) -> str:
    if isinstance(msg, ToolRequestMessage):
        content_lines = [msg.content or ""]
        for tc in msg.tool_calls:
            tcf = tc.function
            content_lines.append(tcf.name + "(" + json.dumps(tcf.arguments) + ")")
        return "\n".join(content_lines)

    return msg.content or ""


class DQNOp(Op):
    network: nn.Module
    target_network: nn.Module
    async_network: AsyncTorchModule
    _network_fwd_args: list[inspect.Parameter]

    CTX_TENSOR_INPUT_KEY: ClassVar[str] = "tensor_input"

    def __init_subclass__(cls) -> None:
        """Register self._network_fwd_args, setup async & target networks."""
        super().__init_subclass__()

        original_init = cls.__init__

        def init_with_network_setup(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            network_fwd_sig = inspect.signature(self.network.forward)
            self._network_fwd_args = list(network_fwd_sig.parameters.values())

            # Set up a helper to handle async forward calls
            if not hasattr(self, "async_network"):
                self.async_network = AsyncTorchModule(
                    self.network, batch_size=8, max_wait_interval=0.01
                )

            # Create a target network if the implementation didn't do so
            if not hasattr(self, "target_network"):
                self.target_network = deepcopy(self.network)

            # Make sure the target network is not trainable
            for param in self.target_network.parameters():
                param.requires_grad = False

        cls.__init__ = init_with_network_setup  # type: ignore[method-assign]

    @contextmanager
    def use_target_network(self):
        self.async_network.module = self.target_network
        yield
        self.async_network.module = self.network

    @abstractmethod
    async def forward(self, state_action: str) -> float:
        pass

    @classmethod
    def backward(
        cls,
        ctx: OpCtx,
        input_args: list[ResultOrValue],
        input_kwargs: dict[str, ResultOrValue],
        grad_output: tree.Structure,
        call_id: CallID,
    ) -> GradInType:
        # DQN does not send gradients back, since we do not need to compute dlnP/dQ
        return assign_constant_grads(input_args, input_kwargs, None)

    def _store_tensor_inputs(
        self,
        tensor_args: Sequence[torch.Tensor],
        tensor_kwargs: Mapping[str, torch.Tensor],
    ):
        # In order to optimize the neural network, we must store its inputs for the
        # optimizer to later use. All subclassed DQNOp.forwards must call this method.
        store_tensor_inputs(
            self.ctx,
            key=self.CTX_TENSOR_INPUT_KEY,
            tensor_args=tensor_args,
            tensor_kwargs=tensor_kwargs,
            fwd_args=self._network_fwd_args,
            detach=True,  # we don't need to backpropagate through the inputs
        )


# Should consider supporting non-Messages, but merge_messages relies on
# this constraint for now.
TAction = TypeVar("TAction", bound=Message)


def merge_messages(state: Sequence[Message], action: Message) -> str:
    all_msgs = [*state, action]
    return "\n".join(get_msg_content(msg) for msg in all_msgs)


class DQNPolicyModule(Generic[TAction]):
    """Module that implements a DQN and epsilon-greedy policy.

    Given a state and list of action candidates, this module will score each action
    and then select an action according to an epsilon-greedy policy. If the set of
    candidate actions is not fixed, but sampled probabilistically, this is
    equivalent to StochDQN (algo 4 of https://arxiv.org/pdf/2405.10310).
    """

    def __init__(
        self, dqn: DQNOp | None = None, epsilon: float = 0.0, actions_only: bool = False
    ):
        self.actions_only = actions_only
        self.merge_messages = FxnOp[str](merge_messages)

        self.dqn = dqn if dqn is not None else EmbeddingDQNOp()

        self.merge_q_action = FxnOp[tuple[float, TAction]](
            lambda q, a: (q, a), fxn_name="merge_q_action"
        )

        self.action_selector = EpsilonGreedyOp(epsilon=epsilon)
        self.action_extractor = FxnOp[TAction](lambda x: x[1])

    @compute_graph()
    async def __call__(
        self,
        state: ResultOrValue[Sequence[Message]],
        *actions: ResultOrValue[TAction],
    ) -> tuple[float, OpResult[TAction]]:
        """Forward pass of the policy.

        Args:
            state: Agent state s_t
            actions: Proposed actions

        Returns:
            (q, a_t): The Q value of the selected action a_t and the
                action itself. We return both in case an agent wants
                to return Q as the value estimate.
        """
        state_actions = await asyncio.gather(*[
            self.merge_messages([] if self.actions_only else state, action)
            for action in actions
        ])
        qs = await asyncio.gather(*[
            self.dqn(state_action) for state_action in state_actions
        ])
        all_qs_and_actions = await asyncio.gather(
            *list(itertools.starmap(self.merge_q_action, zip(qs, actions, strict=True)))
        )

        q_and_action = await self.action_selector(
            *all_qs_and_actions, state_actions=[s_a.value for s_a in state_actions]
        )
        action = await self.action_extractor(q_and_action)
        q = q_and_action.value[0]  # NOTE: q is not part of the compute graph!

        return q, action


def make_regressor(
    input_dim: int,
    hidden_dim: int | list[int],
    num_layers: int,
    dropout: float,
    layer_norm: bool,
    dtype: torch.dtype | str,
) -> nn.Module:
    if num_layers < 1:
        raise ValueError("Must have at least one layer.")

    if num_layers == 1:
        # useful for debugging
        return nn.Linear(input_dim, 1)

    if isinstance(hidden_dim, int):
        hidden_dim = [hidden_dim] * (num_layers - 1)
    if not len(hidden_dim) == num_layers - 1:
        raise ValueError(
            f"Expected {num_layers - 1} hidden dimensions, got {len(hidden_dim)}."
        )

    layers: list[nn.Module] = []
    layers.extend(
        [nn.Linear(input_dim, hidden_dim[0])]
        + ([nn.LayerNorm(hidden_dim[0])] if layer_norm else [])
        + [nn.SiLU(), nn.Dropout(dropout)]
    )
    for i in range(1, num_layers - 1):
        layers.extend(
            [nn.Linear(hidden_dim[i - 1], hidden_dim[i])]
            + ([nn.LayerNorm(hidden_dim[i])] if layer_norm else [])
            + [nn.SiLU(), nn.Dropout(dropout)]
        )
    layers.append(nn.Linear(hidden_dim[-1], 1))
    # initialize the last layer at 0
    layers[-1].weight.data.fill_(0)
    layers[-1].bias.data.fill_(0)

    model = nn.Sequential(*layers)

    if isinstance(dtype, str):
        dtype = getattr(torch, dtype)
    return model.to(dtype)


class EmbeddingDQNOp(DQNOp):
    def __init__(
        self,
        *,
        dense_embedding: str = "text-embedding-3-small",
        dense_embedding_dim: int = 512,
        sparse_embedding_dim: int = 0,
        hidden_dim: int | list[int] = 64,
        num_layers: int = 3,
        dropout: float = 0.0,
        layer_norm: bool = True,
        device: str | torch.device = "cpu",
        dtype: str | torch.dtype = torch.float32,
        fwd_async_batch_size: int = 32,
        fwd_async_max_wait: float = 0.03,
    ):
        emb_models: list[EmbeddingModel] = []
        if dense_embedding_dim > 0:
            emb_models.append(
                LiteEmbeddingModel(
                    name=dense_embedding,
                    dimensions=dense_embedding_dim,
                    embed_kwargs={
                        "caching": True,
                        # LiteLLM docs (https://docs.litellm.ai/docs/proxy/reliability) are not
                        # clear on which to use, and the code appears to deprecate num_retries
                        # for the completions API (but not embeddings). Setting both to be safe
                        # and future-proof. No harm in being reduundant.
                        "max_retries": 5,
                        "num_retries": 5,
                    },
                )
            )
        if sparse_embedding_dim > 0:
            emb_models.append(SparseEmbeddingModel(dimensions=sparse_embedding_dim))
        self.embedding = HybridEmbeddingModel(models=emb_models)

        if isinstance(device, str):
            device = torch.device(device)
        self.device = device

        embedding_dim = dense_embedding_dim + sparse_embedding_dim
        self.network = make_regressor(
            input_dim=embedding_dim,
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            dropout=dropout,
            layer_norm=layer_norm,
            dtype=dtype,
        ).to(device)

        self.async_network = AsyncTorchModule(
            self.network,
            batch_size=fwd_async_batch_size,
            max_wait_interval=fwd_async_max_wait,
        )
        self.async_network = AsyncTorchModule(
            self.network,
            batch_size=fwd_async_batch_size,
            max_wait_interval=fwd_async_max_wait,
        )

    async def forward(self, state_action: str) -> float:
        x = torch.tensor(await self.embedding.embed_text(state_action))
        if get_training_mode():
            self._store_tensor_inputs(tensor_args=(x,), tensor_kwargs={})

        self.async_network.module.eval()
        return (await self.async_network(input=x.to(self.device))).item()


class EpsilonGreedyOp(Op[tuple[float, Message]]):
    """Epsilon-greedy action selection from a list of scored actions.

    In training mode, will pick a random action with probability epsilon. Otherwise,
    greedily picks the highest-scoring action. Gradients only flow back to the selected
    action and corresponding Q value.
    """

    def __init__(self, epsilon: float = 0.0):
        if not 0 <= epsilon <= 1:
            raise ValueError(
                "Epsilon-greedy sampling requires epsilon to be in [0, 1]."
            )
        self.epsilon = epsilon

    async def forward(
        self,
        *scored_actions: tuple[float, Message],
        state_actions: list[str],
    ) -> tuple[float, Message]:
        if get_training_mode() and random.random() < self.epsilon:
            # random
            i_best = random.randint(0, len(scored_actions) - 1)
            best = scored_actions[i_best]

        else:
            # greedy
            i_best, best = max(list(enumerate(scored_actions)), key=lambda x: x[1][0])

        if get_training_mode():
            # Record which we selected. all other branches will be pruned
            # during backward pass
            self.ctx.update(get_call_id(), "i_selected", i_best)
            # Record the (s_t, a_t) candidate pairs for the optimizer to compute
            # max_a' Q(s, a') during the update.
            self.ctx.update(get_call_id(), "state_actions", state_actions)

        return best

    @classmethod
    def backward(
        cls,
        ctx: OpCtx,
        input_args: list[ResultOrValue],
        input_kwargs: dict[str, ResultOrValue],
        grad_output: tree.Structure,
        call_id: CallID,
    ) -> GradInType:
        n_scored_actions = len(input_args)
        i_selected = ctx.get(call_id, "i_selected")
        return (
            [grad_output if i == i_selected else None for i in range(n_scored_actions)],
            {"state_actions": None},
        )
