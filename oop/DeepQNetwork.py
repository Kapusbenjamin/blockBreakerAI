from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class DeepQNetwork:
    def __init__(self, state_size, action_size):
        self.model = self.build_model(state_size, action_size)

    def build_model(self, state_size, action_size):
        model = Sequential()
        model.add(Dense(24, input_dim=state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        return model
