import numpy as np
import random
from DeepQNetwork import *

class Agent:
    def __init__(self, state_size, action_size, max_x, max_y):
        self.state_size = state_size
        self.action_size = action_size
        self.max_x = max_x
        self.max_y = max_y
        self.memory = []
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.model = DeepQNetwork(state_size, action_size)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.array([random.randint(-self.max_x, self.max_x), random.randint(5, self.max_y/2)], dtype=object)
        q_values = self.model.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = np.random.choice(list(self.memory), batch_size, replace=False)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.model.predict(next_state)[0]))
            target_f = self.model.model.predict(state)
            target_f[0][action] = target
            self.model.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
