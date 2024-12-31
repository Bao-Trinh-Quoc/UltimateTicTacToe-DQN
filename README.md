# Ultimate Tic Tac Toe Reinforcement Learning

This project implements an Ultimate Tic Tac Toe game with various agents, including a DQN (Deep Q-Network) agent, a Minimax agent with alpha-beta pruning, and a random agent.

## Requirements
To install the required packages from pipenv, run:
```sh
pipenv install
```

## Usage

### Training the DQN Agent

To train the DQN agent, run:
```sh
python train_test/trainning.py
```

### Testing the Agents

To test the agents, run:
```sh
python train_test/agent_in_single_player_env.py
```

### Playground

To run the playground and evaluate different agents, run:
```sh
python train_test/playground.py
```

## Project Structure

```
UltimateTicTacToe-RL/
├── agents/
│   ├── agent.py
│   ├── agent_dqn.py
│   ├── agent_minimax_pruning.py
│   ├── agent_player.py
│   ├── agent_random.py
│   ├── DQNetwork_final.pt
│   ├── DQNetworkver1_final.pt
│   ├── DQNetwork500_final.pt
├── envs/
│   ├── env_single_player.py
│   ├── env_two_player.py
├── game/
│   ├── board.py
│   ├── ultimatetictactoe.py
├── train_test/
│   ├── agent_in_single_player_env.py
│   ├── playground.py
│   ├── trainning.py
├── Pipfile
├── Pipfile.lock
├── README.md
```

## Agents

- **DQNAgent**: Uses a Deep Q-Network to learn the optimal policy.
- **MinimaxPruningAgent**: Uses the Minimax algorithm with alpha-beta pruning.
- **RandomAgent**: Chooses actions randomly.
- **PlayerAgent**: Allows a human player to interact with the game.

## Environment

The environment is based on the Ultimate Tic Tac Toe game and is implemented using the `gym` library. The main environment classes are:
- `UltimateTicTacToe`: Core game logic and rendering.
- `SinglePlayerEnv`: Environment for training/testing a single agent against a predefined opponent.
- `TwoPlayerEnv`: Environment for two agents playing against each other.

## Training

The training script `train_test/trainning.py` initializes the environment and the DQN agent, and trains the agent using the specified parameters.

## Testing

The testing script `train_test/agent_in_single_player_env.py` allows you to test the trained agents in the Ultimate Tic Tac Toe environment.

## Acknowledgements
https://github.com/JosselinSomervilleRoberts/UltimateTicTacToe-RL
