##During gameplay all the experiences < s, a, r, s’ > are stored in a replay memory.
##In training, batches of randomly drawn experiences are used to generate the input and target for training.
import numpy as np
import os

class ExperienceReplay(object):

    ##max_memory: the maximum number of experiences we want to store
    ##memory: a list of experiences
    ##discount: the discount factor for future experience
    ##information about game ended at the state is stored as nested array.
    ##[ [experience, game_over]
    ##[experience, game_over]  ]
    def __init__(self, max_memory=100000, discount=.9):
        self.max_memory = max_memory
        self.memory = list()
        self.discount = discount

    def remember(self, states, game_over):
        print('\n remember method\n')
        ##Save a state to memory
        self.memory.append([states, game_over])
        ##don't want to store infinite memories, so if have too many then delete the oldest one
        if len(self.memory) > self.max_memory:
            del self.memory[0]

    def get_batch(self, model, batch_size=16):
        print('\n get_batch method\n')
        ##How many experiences to be stored
        len_memory = len(self.memory)

        ##Calculate the number of actions that can possibly be taken in the game
        num_actions = model.output_shape[-1]

        ##Dimensions of the game field
        env_dim = self.memory[0][0][0].shape[1]

        ##want to return an input and target vector with inputs from an observed state
        ##and the target r + gamma * max Q(s’,a’)
        inputs = np.zeros((min(len_memory, batch_size), env_dim))

        ##target is a matrix, with possible fields not only for the action taken but also
        ##for the other possible actions
        targets = np.zeros((inputs.shape[0], num_actions))

        ##draw states to learn from randomly
        for i, idx in enumerate(np.random.randint(0, len_memory,size=inputs.shape[0])):
            
            ##load one transition <s, a, r, s’> from memory
            ##state_t: initial state s,action_t: action taken a,reward_t: reward earned r,state_tp1: state followed s’
            state_t, action_t, reward_t, state_tp1 = self.memory[idx][0]

            ##need to know whether the game ended at this state
            game_over = self.memory[idx][1]

            ##add the state s to the input
            inputs[i:i + 1] = state_t

            ##Fill the target values with the predictions of the model.
            targets[i] = model.predict(state_t)[0]

            ## Q_sa is max_a'Q(s', a')
            Q_sa = np.max(model.predict(state_tp1)[0])

            ##If the game ended, the expected reward Q(s,a) should be the final reward r.
            if game_over:
                print('game_over condition')
                targets[i, action_t] = reward_t
            ##Otherwise the target value is r + gamma * max Q(s’,a’)
            else:
                print('game_over else condition')
                targets[i, action_t] = reward_t + self.discount * Q_sa
        return inputs, targets
