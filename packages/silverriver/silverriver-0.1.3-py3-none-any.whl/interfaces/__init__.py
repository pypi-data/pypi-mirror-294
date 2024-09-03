import pydantic

from silverriver.interfaces.base_agent import AgentAction
from silverriver.interfaces.data_models import Observation


class SubTransition(pydantic.BaseModel, extra="forbid"):
    # obs is purposely different from observation to ensure the two Transitions are not interchangeable
    obs: dict = pydantic.Field(default_factory=dict)
    reward: float = 0.
    done: bool = False
    info: dict = pydantic.Field(default_factory=dict)

    def __add__(self, other: 'SubTransition') -> 'SubTransition':
        assert not set(self.obs.keys()) & set(other.obs.keys()), f"Overlapping keys: {set(self.obs.keys()) & set(other.obs.keys())}"
        assert not set(self.info.keys()) & set(other.info.keys()), f"Overlapping keys: {set(self.info.keys()) & set(other.info.keys())}"
        return SubTransition(
            obs={**self.obs, **other.obs},
            reward=self.reward + other.reward,
            done=self.done or other.done,
            info={**self.info, **other.info}
        )


class TransitionObservation(pydantic.BaseModel, extra="forbid"):
    # An observation is everything the agent should be aware of.
    observation: Observation
    reward: float
    done: bool
    # Info contains anything that systems around the agent need but not the agent itself
    # It's purposefully not typed to allow for flexibility.
    info: dict


class SetupInput(pydantic.BaseModel, extra="forbid"):
    start_url: str


class SetupOutput(pydantic.BaseModel, extra="forbid"):
    init_acts: tuple[AgentAction, ...] = tuple()
    exec_context: dict = pydantic.Field(default_factory=dict)
