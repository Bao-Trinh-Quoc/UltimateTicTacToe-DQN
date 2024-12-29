import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from envs.env_single_player import SinglePlayerEnv
from agents.agent_minimax_pruning import MinimaxPruningAgent
from agents.agent_random import RandomAgent
from agents.agent_dqn import DQNAgent

# Initialize the environment with a RandomAgent as the opponent
# agent2 = RandomAgent(2)
agent2 = MinimaxPruningAgent(2, 4, True)
env = SinglePlayerEnv(agent2)

# Initialize the DQNAgent
agent = DQNAgent(1, env, loading=True, name="ver1")

# Train the agent
agent.learnNN(env, masked=False, n_episodes=1000, n_save=3000, trainingName="ver1")

if __name__ == '__main__':
    obs = env.reset()
    done = False

    while not done:
        # Ask the agent to choose an action
        action = agent.getAction(env, obs)

        # If the action is negative, this means that the agent asks to close the game
        if action < 0:
            done = True

        # Otherwise, if the action is valid, we play it in the env
        elif action < 81:
            obs, reward, done, info = env.step(action)

    print("ENV state:", env.pygame.board.state)
    env.close()