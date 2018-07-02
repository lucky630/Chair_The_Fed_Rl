##this is the main class which will load model and decide
##whether to train or test the model.
import numpy as np
import pytesseract as pt
from keras.layers.core import Dense
from keras.models import Sequential
from keras.models import model_from_json
from keras.optimizers import sgd
from matplotlib import pyplot as plt
from CHAIRFED import CHAIRFED
from train_model import train
from test_model import test

##two layer sequential model used to train for mapping the state with action.
##grid size is the state dimension and num_actions are the output target.
def baseline_model(grid_size, num_actions, hidden_size):
    # setting up the model with keras
    model = Sequential()
    model.add(Dense(hidden_size, input_shape=(grid_size,), activation='relu'))
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dense(num_actions))
    model.compile(sgd(lr=.01), "mse")
    return model


def moving_average_diff(a, n=100):
    diff = np.diff(a)
    ret = np.cumsum(diff, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

##load the already saved model
def load_model():
    # load json and create model
    print('loading already saved model..')
    json_file = open('saved_model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("saved_model/model.h5")
    print("Loaded model from disk")
    loaded_model.compile(loss='mse', optimizer='sgd')
    return loaded_model

#model = baseline_model(grid_size=128, num_actions=8, hidden_size=512)
# model = baseline_model(grid_size=4, num_actions=8, hidden_size=100)
model = load_model()
model.summary()

pt.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

print('started!!!')

##create the game object
game = CHAIRFED()
print("game object created")

epoch = 2  # Number of games played in training,

##switch to toggle between train and test. 
train_mode = 0

if train_mode == 1:
    # Train the model
    hist,loss = train(game, model, epoch, verbose=1)
    print(loss)
    np.savetxt('loss_history.txt', loss)
    print("Training done")
else:
    # Test the model
    hist = test(game, model, epoch, verbose=1)
    print("Testing done")

print('finished!!!')
print(hist)
np.savetxt('win_history.txt', hist)
plt.plot(moving_average_diff(hist))
plt.ylabel('Average number of stableness per quater')
plt.show()
