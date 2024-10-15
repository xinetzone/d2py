from gymnasium.envs.registration import register


# Collect game with 2 agents and 3 object types
# ----------------------------------------
register(
    id="multigrid-collect-v0",
    entry_point="gym_multigrid.envs:CollectGameEvenDist",
    max_episode_steps=100,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": False,
    },
)

# Collect game with single agent and 3 object types
# ----------------------------------------
register(
    id="multigrid-collect-single-v0",
    entry_point="gym_multigrid.envs:CollectGameEvenDist",
    max_episode_steps=100,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3],  # green
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": False,
    },
)

# Collect game with 2 agents and 3 object types clustered in different quadrants of the grid
# ----------------------------------------
register(
    id="multigrid-collect-quadrants-v0",
    entry_point="gym_multigrid.envs:CollectGameQuadrants",
    max_episode_steps=100,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": False,
    },
)

# Collect game with 2 agents and 3 object types clustered in four rooms
# ----------------------------------------
register(
    id="multigrid-collect-rooms-v0",
    entry_point="gym_multigrid.envs:CollectGameRooms",
    max_episode_steps=100,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": False,
    },
)

# Collect game with 2 agents and 3 object types clustered differently in four rooms
# Episode has a fixed horizon instead of terminating after collecting all objects
# ----------------------------------------
register(
    id="multigrid-collect-rooms-fixed-horizon-v0",
    entry_point="gym_multigrid.envs:CollectGameRoomsFixedHorizon",
    max_episode_steps=100,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": False,
    },
)

# Collect game with 2 agents and 3 object types clustered differently in four rooms
# Episode has a fixed horizon and objects respawn after collection
# ----------------------------------------
register(
    id="multigrid-collect-rooms-respawn-v0",
    entry_point="gym_multigrid.envs:CollectGameRoomsFixedHorizon",
    max_episode_steps=50,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": True,
    },
)

# Collect game with 2 agents and 3 object types
# Episode has a fixed horizon and objects respawn after collection
# ----------------------------------------
register(
    id="multigrid-collect-respawn-v0",
    entry_point="gym_multigrid.envs:CollectGameEvenDist",
    max_episode_steps=50,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": True,
    },
)

# Collect game with 2 agents and 3 object types clustered in different quadrants of the grid
# Episode has a fixed horizon and objects respawn after collection
# ----------------------------------------
register(
    id="multigrid-collect-respawn-clustered-v0",
    entry_point="gym_multigrid.envs:CollectGameQuadrantsRespawn",
    max_episode_steps=50,
    kwargs={
        "size": 10,
        "num_balls": 15,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": True,
    },
)

register(
    id="multigrid-collect-quadrants15-v0",
    entry_point="gym_multigrid.envs:CollectGameQuadrants",
    kwargs={
        "size": 15,
        "num_balls": 30,
        "agents_index": [3, 5],  # green, purple
        "balls_index": [0, 1, 2],  # red, orange, yellow
        "balls_reward": [1, 1, 1],
        "respawn": False,
    },
)