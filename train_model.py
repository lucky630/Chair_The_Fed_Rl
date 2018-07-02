##This class used to train the model for the specified number of epochs.
##
import numpy as np
import time
from ExperienceReplay import ExperienceReplay
from Game_util_selenium import *

# parameters
# epsilon = .2  # exploration
num_actions = 8  # [ 1, 2, 3, 4, 5, 6, 7, 8]
max_memory = 1000  # Maximum number of experiences we are storing
batch_size = 15  # Number of experiences we use for training per batch

##ExperienceReplay class will store the experiences as < s, a, r, s’ >
exp_replay = ExperienceReplay(max_memory=max_memory)

chromedriver = "C:\\Users\\royal\\Downloads\\Programs\\chromedriver_win32\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

##save the model after every epoch.
def save_model(model):
    # serialize model to JSON
    model_json = model.to_json()
    with open("saved_model/model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("saved_model/model.h5")
    # print("Saved model to disk")

def train(game, model, epochs, verbose=1):
    # Reseting the win counter
    win_cnt = 0
    # save the win count history
    win_hist = []
    # save the loss history
    loss_hist = []
    # Epochs is the number of games we play 1,16 quarters are considered as 1 game.
    for e in range(epochs):
        loss = 0.
        #epsilon = 4 / ((e + 1) ** (1 / 2))
        epsilon = 2 / ((e + 1) ** (1 / 2))
        # Resetting the game
        game.reset()
        game_over = False
	##first time then start the browser and game with selenium
        if e == 0:
            print('Training is started. game is loaded and is ready to be played.')
            open_page_start(driver)
            time.sleep(12)
        else:
            print('Game is played. at epoch '+str(e))
        ##get the first state from env.
        input_t = game.observe(driver)
        while not game_over:
            # The learner is acting on the last observed game screen
            # input_t is a vector containing representing the game screen
            input_tm1 = input_t
            #The chance that Agent take Random action is epsilon.
            if np.random.rand() <= epsilon:
                # do some random action.
                action = int(np.random.randint(0, num_actions, size=1))
                print('random action: '+str(action))
            else:
                # non random action
                # q contains the expected rewards for the actions
                q = model.predict(input_tm1)
                print('q values=' + str(q[0]))
                # We pick the action with the highest expected reward
                action = np.argmax(q[0])
            # apply action, get rewards and new state
            input_t, reward, game_over = game.act(action,driver)
            # If we managed to get the positive reward we add 1 to our win counter
            if reward == 1:
                win_cnt += 1

            #Here we first save the last experience, and then load a batch of experiences to train our model
            exp_replay.remember([input_tm1, action, reward, input_t], game_over)

            # Load batch of experiences
            inputs, targets = exp_replay.get_batch(model, batch_size=batch_size)

            # train model on experiences
            batch_loss = model.train_on_batch(inputs, targets)

            # print(loss)
            loss += batch_loss

        loss_hist.append(loss)
        if verbose > 0:
            print("Epoch {:03d}/{:03d} | Loss {:.4f} | Win count {}".format(e, epochs, loss, win_cnt))
        save_model(model)
        win_hist.append(win_cnt)
    return win_hist,loss_hist
