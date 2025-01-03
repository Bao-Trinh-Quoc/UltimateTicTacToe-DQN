# from html.entities import name2codepoint
from agents.agent import Agent

import gym
import numpy as np
import torch
from torch.optim import Adam
from torch.nn import Linear, ReLU, Dropout, BatchNorm1d
import os
import tqdm



class DQNetwork(torch.nn.Module):
    def __init__(self, state_len, n_actions,learning_rate):
        super(DQNetwork, self).__init__()
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print(self.device)
        self.learning_rate = learning_rate
        self.n_actions = n_actions
        self.network = torch.nn.Sequential(
            torch.nn.Linear(state_len, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, n_actions)
        )
        self.optimizer = Adam(self.parameters(), lr = learning_rate)
        self.loss = torch.nn.MSELoss(reduction='sum')
        self.to(self.device)


    def forward(self,state):
        return self.network(state)

    def save(self, name = ""):
        torch.save(self,os.path.dirname(__file__)+"/DQNetwork" + name + ".pt")

    def load(self, name = ""):
        self = torch.load(os.path.dirname(__file__)+"/DQNetwork" + name + ".pt")
        self.eval()


# Process the observation from the environment to a format that can be used by the neural network
def processObs(observation):
    return np.array(observation[0] + observation[1] +[1 if i in observation[2] else 0 for i in range(9)]).flatten()

# Store experiences and sample them for training
class ReplayBuffer(object):
    def __init__(self, state_len, mem_size):
        self.state_len = state_len
        self.mem_size = mem_size
        self.mem_counter = 0
        self.states = np.zeros((mem_size, state_len), dtype=np.float32)
        self.actions = np.zeros(mem_size, dtype=np.int32)
        self.rewards = np.zeros(mem_size, dtype=np.float32)
        self.new_states = np.zeros((mem_size, state_len), dtype=np.float32)
        self.dones = np.zeros(mem_size, dtype=np.int32)


    def store_transition(self, state, action, reward, new_state, done):
        index = self.mem_counter%self.mem_size
        self.states[index, :] = state
        self.actions[index] = action
        self.rewards[index] = reward
        self.new_states[index, :] = new_state
        self.dones[index] = done
        self.mem_counter += 1

    def sample_memory(self, batch_size):
        max_memory = min(self.mem_size, self.mem_counter)
        batch = np.random.choice(np.arange(max_memory), batch_size, replace=False)
        states = self.states[batch, :]
        actions = self.actions[batch]
        rewards = self.rewards[batch]
        new_states = self.new_states[batch, :]
        dones = self.dones[batch]
        return states, actions, rewards, new_states, dones


class DQNAgent(Agent):

    def __init__(self, player = 1, env = gym.make('LunarLander-v2'), loading=True, name = ""):

        learning_rate=0.00005
        gamma=0.99
        batch_size=64
        state_len=99
        n_actions = env.action_space.n
        mem_size = 1000000
        min_memory_for_training=1000
        epsilon=0.3
        epsilon_dec=0.998
        epsilon_min = 0.1
        # frozen_iterations=6


        super().__init__(self)
        self.it_counter = 0            # how many timesteps have passed already
        self.gamma = gamma             # gamma hyperparameter
        self.batch_size = batch_size   # batch size hyperparameter for neural network
        self.state_len = state_len     # how long the state vector is
        self.n_actions = n_actions     # number of actions the agent can take
        self.epsilon = epsilon         # epsilon start value (1=completly random)
        self.epsilon_min = epsilon_min # the minimum value
        self.epsilon_dec = epsilon_dec
        self.mem_size = mem_size

        self.min_memory_for_training = min_memory_for_training
        self.q = DQNetwork(state_len, 81, learning_rate)
        self.replay_buffer = ReplayBuffer(self.state_len, mem_size)

        if loading :
            self.q.load(name)
        else :
            self.learnNN(env)

    def getAction(self, env, observation, check_validity = True):
        observation = torch.tensor(processObs(observation), dtype = torch.float32).to(self.q.device)
        q = self.q.forward(observation)
        action = int(torch.argmax(q))

        if check_validity:
            # checks for action validity
            valid_actions = env.valid_actions()

            if action in valid_actions:
                pass
            else:
                q_min = float(torch.min(q))
                mask = np.array([True if i in valid_actions else False for i in range(env.action_space.n)])
                # new_q = (q.detach().numpy() - q_min + 1.) *  mask
                new_q = (q.detach().cpu().numpy() - q_min + 1.) * mask
                action = int(np.argmax(new_q))

        # value = q[action]
        # print("picked action : ",action," reward : ", value)
        return action

    def pickActionMaybeRandom(self, env, observation, check_validity = False):
        if np.random.random() < self.epsilon:
            valid_actions = env.valid_actions()
            return int(np.random.choice(valid_actions))
        else:
            return self.getAction(env, observation, check_validity)

    def pickActionMaybeMasked(self, env, observation):
        if np.random.random() < self.epsilon:
            return self.getAction(env, observation, True)
        else:
            return self.getAction(env, observation, False)

    def learn(self, error):
        if self.replay_buffer.mem_counter < self.min_memory_for_training:
            return
        
        states, actions, rewards, new_states, dones = self.replay_buffer.sample_memory(self.batch_size)
        self.q.optimizer.zero_grad()
        states_batch = torch.tensor(states, dtype = torch.float32).to(self.q.device)
        new_states_batch = torch.tensor(new_states,dtype = torch.float32).to(self.q.device)
        actions_batch = torch.tensor(actions, dtype = torch.long).to(self.q.device)
        rewards_batch = torch.tensor(rewards, dtype = torch.float32).to(self.q.device)
        dones_batch = torch.tensor(dones, dtype = torch.float32).to(self.q.device)
        
        # Bellman equation
        target = rewards_batch + torch.mul(self.gamma* self.q(new_states_batch).max(axis = 1).values, (1 - dones_batch))
        prediction = self.q.forward(states_batch).gather(1,actions_batch.unsqueeze(1)).squeeze(1)

        loss = self.q.loss(prediction, target)
        loss.backward()                 # Compute gradients
        self.q.optimizer.step()         # Backpropagate error

        # decrease epsilon:
        if error == 0:
            if self.epsilon * self.epsilon_dec > self.epsilon_min:
                self.epsilon *= self.epsilon_dec
        else:
            if self.epsilon / self.epsilon_dec <= 1:
                self.epsilon /= self.epsilon_dec

        self.it_counter += 1
        return

    def learnNN(self, env, masked = False, n_episodes = 100, n_save = 1000, trainingName = ""):
        l_epsilon = []
        l_win = []
        sum_win = 0

        for episode in tqdm.tqdm(range(n_episodes)):
            state = env.reset()         # resetting the environment after each episode
            score = 0
            done = 0
            while not done:               # while the episode is not over yet
                action = None
                if masked:
                    action = self.getAction(env, state, True)
                else:
                    action = self.pickActionMaybeMasked(env,state)              # let the agent act
                new_state,reward, done, error = env.step(action)                # performing the action in the environment
                score += reward                                                 # the total score during this round
                self.replay_buffer.store_transition(processObs(state), action, reward, processObs(new_state), done)   # store timestep for experiene replay
                self.learn(error)                                               # the agent learns after each timestep
                state = new_state

            if env.pygame.board.state == 1:
                sum_win +=1
            elif env.pygame.board.state == 2:
                sum_win -= 1
            elif env.pygame.board.state == 3:
                sum_win += 0

            l_epsilon.append(self.epsilon)
            l_win.append(sum_win)

            if (episode+1) % n_save == 0:
                self.q.save(trainingName + "_" + str(episode+1))

        env.close()
        self.q.save(trainingName + "_final")
        print(l_epsilon)
        print("\n")
        print(l_win)