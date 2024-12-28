import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from envs.env_single_player import SinglePlayerEnv
import pygame

from agents.agent_player import PlayerAgent
from agents.agent_random import RandomAgent
from agents.agent_minimax_pruning import MinimaxPruningAgent
from agents.agent_dqn import DQNAgent




# agent = DQNAgent(1)
agent = DQNAgent(1, loading=True, name="ver1_final")
#agent = RandomAgent(1)
#agent = MinimaxPruningAgent(1, 3, True)
#agent = MinimaxPruningAgent(1, 5, True)



display = True
if __name__ == '__main__':
    agent2 =  PlayerAgent(2)
    env = SinglePlayerEnv(agent2)
    obs = env.reset()

    done = False
    game = True
    while game:

        if not(done):
            # Ask the agent to choose an action
            action = agent.getAction(env, obs)

            # If the aciton is negative this means that the agent asks to close the game
            if action < 0:
                done = True

            # Otherwise, if the action is valid we play it in the env
            elif action < 81:
                obs, reward, done, info = env.step(action)

        if display:
            # Render the environment
            env.render()

            # Check for pygame event (to close the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False

            # Delay to not spam
            pygame.time.delay(1)

    pygame.quit()
    print("ENV state:", env.pygame.board.state)
    env.close()