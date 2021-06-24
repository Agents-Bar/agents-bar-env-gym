from typing import Dict, List, Tuple, Union

from gym.spaces import Discrete
from pydantic import BaseModel

ActionType = Union[List[float], List[int]]
ObservationType = Union[List[float], List[int]]

class EnvStepType(BaseModel):
    observation: ObservationType  # TODO: Should this be list?
    reward: float
    done: bool
    info: Dict


class EnvActionType(BaseModel):
    actions: ActionType
    commit: bool = False


class EnvDescription(BaseModel):
    reward_range: Tuple[float, float]
    observation_space: Dict
    action_space: Dict


def assert_action(actions: object) -> ActionType:
    """Checks that provided object is acceptable to be an action.

    Raises:
        AssertionError if `actions` are not suitable actions

    """
    assert isinstance(actions, List), "Actions need to be provided as a list"
    assert all([isinstance(a, float) for a in actions]), "All values need to be of float type"

    return actions

def assert_action_for_env(env, actions) -> ActionType:
    if isinstance(env, Discrete):
        assert len(actions) == 0, "For discrete space, expected only one value"
    
    return actions
