import os

import numpy as np
import imageio

from gym_multigrid.envs.ctf import Ctf1v1Env, CtFMvNEnv
from gym_multigrid.policy.ctf.heuristic import (
    FightPolicy,
    CapturePolicy,
    PatrolPolicy,
    RwPolicy,
    PatrolFightPolicy,
)
from gym_multigrid.utils.map import load_text_map
import matplotlib.pyplot as plt


def test_ctf() -> None:
    map_path: str = "tests/assets/board.txt"

    env = Ctf1v1Env(
        map_path=map_path, render_mode="human", observation_option="flattened"
    )
    obs, _ = env.reset()
    env.render()

    while True:
        action = np.random.choice(list(env.actions_set))
        obs, reward, terminated, truncated, info = env.step(action)
        env.render()
        if terminated or truncated:
            break


# TODO: might be good idea to include seeding test for other environments
def test_ctf_random_seeding() -> None:
    map_path: str = "tests/assets/board.txt"
    env = Ctf1v1Env(
        map_path=map_path, render_mode="human", observation_option="flattened"
    )
    env.reset(seed=1)
    array1 = env.np_random.random(10)
    env.reset(seed=1)
    array2 = env.np_random.random(10)

    np.testing.assert_allclose(array1, array2)


# MvN CtF test
def test_ctf_mvn_human() -> None:
    map_path: str = "tests/assets/board.txt"
    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="human",
        observation_option="flattened",
    )
    obs, _ = env.reset()
    env.render()

    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        env.render()
        if terminated or truncated:
            break

    assert terminated or truncated


def test_ctf_mvn_rgb() -> None:
    map_path: str = "tests/assets/board.txt"
    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="rgb_array",
        observation_option="flattened",
    )
    obs, _ = env.reset()
    frames = [env.render()]
    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break

    imageio.mimsave("tests/out/animations/ctf_mvn.gif", frames, duration=0.5)

    assert os.path.exists("tests/out/animations/ctf_mvn.gif")


def test_fight_policy() -> None:
    animation_path: str = "tests/out/animations/ctf_mvn_fight_policy.gif"
    map_path: str = "tests/assets/board.txt"

    field_map = load_text_map(map_path)
    enemy_policy = FightPolicy()

    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="human",
        observation_option="flattened",
        enemy_policies=[enemy_policy, RwPolicy()],
    )

    obs, _ = env.reset()
    frames = [env.render()]
    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break

    imageio.mimsave(animation_path, frames, duration=0.5)

    assert os.path.exists(animation_path)


def test_capture_policy() -> None:
    animation_path: str = "tests/out/animations/ctf_mvn_capture_policy.gif"
    map_path: str = "tests/assets/board.txt"

    field_map = load_text_map(map_path)
    enemy_policy = CapturePolicy(field_map)

    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="human",
        observation_option="flattened",
        enemy_policies=[enemy_policy, RwPolicy()],
    )

    obs, _ = env.reset()
    frames = [env.render()]
    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break

    imageio.mimsave(animation_path, frames, duration=0.5)

    assert os.path.exists(animation_path)


def test_patrol_policy() -> None:
    animation_path: str = "tests/out/animations/ctf_mvn_patrol_policy.gif"
    map_path: str = "tests/assets/board.txt"

    field_map = load_text_map(map_path)
    enemy_policy = PatrolPolicy(field_map)

    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="human",
        observation_option="flattened",
        enemy_policies=enemy_policy,
    )

    obs, _ = env.reset()
    frames = [env.render()]
    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break

    imageio.mimsave(animation_path, frames, duration=0.5)

    assert os.path.exists(animation_path)


def test_patrol_fight_policy() -> None:
    animation_path: str = "tests/out/animations/ctf_mvn_patrol_fight_policy.gif"
    map_path: str = "tests/assets/board.txt"

    field_map = load_text_map(map_path)
    enemy_policy = PatrolFightPolicy(field_map)

    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="human",
        observation_option="flattened",
        enemy_policies=enemy_policy,
    )

    obs, _ = env.reset()
    frames = [env.render()]
    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        frames.append(env.render())
        if terminated or truncated:
            break

    imageio.mimsave(animation_path, frames, duration=0.5)

    assert os.path.exists(animation_path)


def test_mvn_ctf_render() -> None:
    img_save_path: str = "tests/out/plots/mvn_ctf_render.png"
    map_path: str = "tests/assets/board.txt"
    env = CtFMvNEnv(
        num_blue_agents=2,
        num_red_agents=2,
        map_path=map_path,
        render_mode="human",
        observation_option="flattened",
    )
    obs, _ = env.reset()

    for _ in range(1):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

    img = env.render()
    plt.imsave(img_save_path, img, dpi=600)

    assert os.path.exists(img_save_path)
