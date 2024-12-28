import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from envs.env_single_player import SinglePlayerEnv
from agents.agent_random import RandomAgent
from agents.agent_dqn import DQNAgent

# Initialize the environment with a RandomAgent as the opponent
agent2 = RandomAgent(2)
env = SinglePlayerEnv(agent2)

# Initialize the DQNAgent
# agent = DQNAgent(1, env, loading=True, name="")
agent = DQNAgent(1, env, loading=False, name="")

# Train the agent
agent.learnNN(env, masked=False, n_episodes=500, n_save=1500, trainingName="500")

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