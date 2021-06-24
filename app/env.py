import logging
import sys
from typing import Optional

import gym
from fastapi import APIRouter, HTTPException
from gym.spaces.discrete import Discrete

from app.types import (ActionType, EnvActionType, EnvStepType, ObservationType,
                       assert_action, assert_action_for_env)
from app.utils import to_list

# Initiate module with setting up a server
router = APIRouter()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


env: Optional[gym.Env] = None
last_step: Optional[EnvStepType] = None


@router.post("/env", status_code=201)
def create_env(gym_name: str):
    "Create environment based on the OpenAI Gym"
    global env
    try:
        env = gym.make(gym_name)
        if env is not None:
            return {"msg": "Env created successfully"}
        else:
            raise HTTPException(500, "Something went wrong.")
    except gym.error.Error as e:
        raise HTTPException(400, str(e))


@router.post('/env/reset', response_model=ObservationType)
def reset_env() -> ObservationType:
    "Reset the environment to initial position."
    global env
    env = check_env(env)
    observation = env.reset()
    obs = to_list(observation)
    return obs


@router.post("/env/step", response_model=Optional[EnvStepType])
def post_step(env_action: EnvActionType):
    "Provides information necessary to step the environment."
    global env, last_step, last_actions
    env = check_env(env)
    try:
        last_actions = assert_action(env_action.actions)
        last_actions = assert_action_for_env(env, last_actions)
    except AssertionError as ae:
        raise HTTPException(400, ae)

    if env_action.commit:
        last_step = commit(env, last_actions)
        return last_step

    return None

@router.post('/env/commit', response_model=EnvStepType)
def post_commit() -> EnvStepType:
    "Commit last sent step data."
    global env, last_actions, last_step
    env = check_env(env)
    last_step = commit(env, last_actions)
    return last_step


@router.get('/env/last', response_model=EnvStepType)
def get_last() -> EnvStepType:
    "Retrieve last provided Step data."
    if last_step is None:
        raise HTTPException(404, detail="No environment information to return")
    return last_step

@router.post('/env/seed')
def set_seed(seed: int) -> None:
    "Set seed for environment's random number generator."
    global env
    env = check_env(env)
    env.seed(seed)
    return None


def check_env(env: Optional[gym.Env]) -> gym.Env:
    """Make sure env (environment) is defined correctly.
    Intended to use directly and shortly after receiving API call.

    Raises:
        HTTPException if there is anything wrong with provided environment.

    """
    if env is None:
        raise HTTPException(400, detail="Environment is not instantiated.")
    return env


def commit(env: gym.Env, actions: ActionType) -> EnvStepType:
    """Logic part that commits data to environment engine.

    Raises:
        HTTPException if there is anything wrong with provided data either before
        or after passing to the environment.

    """
    if isinstance(env.action_space, Discrete):
        logging.info("Discrete")
        actions = int(actions[0])  # TODO: Make this better.

    try:
        out = env.step(actions)
    except Exception as e:
        logging.exception("Something wrong while commiting step")
        raise HTTPException(500, str(e))
    obs = to_list(out[0])
    step = EnvStepType(observation=obs, reward=out[1], done=out[2], info=out[3])
    return step