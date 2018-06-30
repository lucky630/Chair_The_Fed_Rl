import time
import numpy as np
from Game_util_selenium import *

chromedriver = "C:\\Users\\royal\\Downloads\\Programs\\chromedriver_win32\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

def test(game, model, n_games, verbose=1):
    # Test
    # Reseting the win counter
    win_cnt = 0
    # We want to keep track of the progress of the AI over time, so we save its win count history
    win_hist = []
    # Epochs is the number of games we play
    for e in range(n_games):
        # Resetting the game
        game.reset()
        game_over = False
        if e == 0:
            print('Testing started. game is loaded and is ready to be played.')
            open_page_start(driver)
        else:
            print('Game is played. at epoch '+str(e))
        input_t = game.observe(driver)
        while not game_over:
            # The learner is acting on the last observed game screen
            input_tm1 = input_t
            # q contains the expected rewards for the actions
            q = model.predict(input_tm1)
            # We pick the action with the highest expected reward
            print('q values=' + str(q[0]))
            action = np.argmax(q[0])
            # apply action, get rewards and new state
            input_t, reward, game_over = game.act(action,driver)
            # If we managed to catch the fruit we add 1 to our win counter
            if reward == 1:
                win_cnt += 1
        if verbose > 0:
            print("Game {:03d}/{:03d} | Win count {}".format(e, n_games, win_cnt))
        win_hist.append(win_cnt)
    return win_hist
