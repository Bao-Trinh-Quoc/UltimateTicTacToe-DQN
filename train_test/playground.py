import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from envs.env_single_player import SinglePlayerEnv
from agents.agent_dqn import DQNAgent
from agents.agent_minimax_pruning import MinimaxPruningAgent
from agents.agent_random import RandomAgent
import tqdm

env = SinglePlayerEnv(RandomAgent(2))

# DQNAgent(2, env, loading=True, name="500_final")
agents1 = [
    DQNAgent(1, env, loading=True, name="ver1_final")
    # MinimaxPruningAgent(1, 3, True)
    # RandomAgent(1)
]

agents2 = [
    RandomAgent(2)
    # MinimaxPruningAgent(2, 3, True)
]

if __name__ == '__main__':
    N = 100
    n = len(agents1)
    wins = [[0 for i in range(n)] for j in range(n)]
    equalities = [[0 for i in range(n)] for j in range(n)]
    losses = [[0 for i in range(n)] for j in range(n)]

    for it in tqdm.tqdm(range(N)):
        for i1 in range(n):
            for i2 in range(n):
                agent1 = agents1[i1]
                agent2 = agents2[i2]
                
                env.agent1 = agent1
                env.agent2 = agent2
                obs = env.reset()

                done = False
                while not done:
                    # Ask the agent to choose an action
                    action = agent1.getAction(env, obs)

                    # If the action is negative, this means that the agent asks to close the game
                    if action < 0:
                        done = True

                    # Otherwise, if the action is valid, we play it in the env
                    elif action < 81:
                        obs, reward, done, info = env.step(action)

                if env.pygame.board.state == 1:
                    wins[i1][i2] += 1
                elif env.pygame.board.state == 2:
                    losses[i1][i2] += 1
                elif env.pygame.board.state == 3:
                    equalities[i1][i2] += 1

    print("First agent: ", agents1)
    print("Second agent: ", agents2)
    print("First agent wins:")
    print(wins)
    print("\nSecond agent wins:")
    print(losses)
    print("\nDraws:")
    print(equalities)

    env.close()


# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from envs.env_two_player import TwoPlayerEnv
# from agents.agent_dqn import DQNAgent
# import pygame

# # Initialize the environment
# env = TwoPlayerEnv()

# agent1 = DQNAgent(1, env, loading=True, name="ver1_final")
# agent2 = DQNAgent(2, env, loading=True, name="500_final") 

# def play_game(agent1, agent2, env):
#     obs = env.reset()
#     done = False

#     while not done:
#         # Agent 1's turn
#         action1 = agent1.getAction(env, obs)
#         if action1 < 0:
#             done = True
#         elif action1 < 81:
#             obs, reward, done, info = env.step(action1)

#         if done:
#             break

#         # Agent 2's turn
#         action2 = agent2.getAction(env, obs)
#         if action2 < 0:
#             done = True
#         elif action2 < 81:
#             obs, reward, done, info = env.step(action2)

#     return env.pygame.board.state

# if __name__ == '__main__':
#     N = 20  # Number of games to play
#     results = {"Agent 1 Wins": 0, "Agent 2 Wins": 0, "Draws": 0}

#     for _ in range(N):
#         result = play_game(agent1, agent2, env)
#         if result == 1:
#             results["Agent 1 Wins"] += 1
#         elif result == 2:
#             results["Agent 2 Wins"] += 1
#         elif result == 3:
#             results["Draws"] += 1

#     env.close()
#     pygame.quit()

#     print(f"Results after {N} games:")
#     print(f"Agent 1 Wins: {results['Agent 1 Wins']}")
#     print(f"Agent 2 Wins: {results['Agent 2 Wins']}")
#     print(f"Draws: {results['Draws']}")