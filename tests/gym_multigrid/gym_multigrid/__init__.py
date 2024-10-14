from gymnasium.envs.registration import register

register(
    id="gym_multigrid/GridWorld-v0",
    entry_point="gym_multigrid.envs:GridWorldEnv",
)
