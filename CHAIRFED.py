import numpy as np
import pytesseract as pt
from STATE import STATE
from Game_util_selenium import *
from selenium import webdriver

class CHAIRFED(object):
	
    state_graph = STATE()
    reward = 0

    def __init__(self):
        self.reset()

    def _get_reward(self, driver):
        print('\n get reward method\n')
        screen = screen_grab(driver)
        fed=float(''.join(get_fed_rates(screen).split()).split('%')[0])
        unemp=float(''.join(get_unemploy_rate(screen).split()).split('%')[0])
        infl=float(''.join(get_inflate_rate(screen).split()).split('%')[0])
        ingame_reward=-10
        if (unemp > 4.0 and unemp < 6.0) and (infl > 1.0 and infl < 3.0):
            ingame_reward = 1
        else:
            ingame_reward = -1
        print('q-learning reward: ' + str(ingame_reward))
        return ingame_reward

    def _is_over(self, action):
        print('\n is_over method\n')
        is_over = True if action in [0, 1, 2, 3, 4, 5, 6, 7] else False
        return is_over

    def observe(self,driver):
        print('\n observe method\n')
        # get current state s from screen using screen_grab
        screen = screen_grab(driver)
        fed=float(''.join(get_fed_rates(screen).split()).split('%')[0])
        unemp=float(''.join(get_unemploy_rate(screen).split()).split('%')[0])
        infl=float(''.join(get_inflate_rate(screen).split()).split('%')[0])
        news=' '.join(get_news(screen).split('\n'))

        data=str(fed)+','+str(unemp)+','+str(infl)+','+news
        print(data)
        # process through state_graph to get the state.
        state = self.state_graph.get_features_128(news,fed,unemp,infl)
        return state

    def act(self, action, driver):
        print('\n act method\n')
        display_action = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        print('action: ' + str(display_action[action]))
        screen = screen_grab(driver)
        
        fed=float(''.join(get_fed_rates(screen).split()).split('%')[0])
        set_fed_rate(driver,fed,display_action[action])

        reward = self._get_reward(driver)
        game_over = self._is_over(action)
        return self.observe(driver), reward, game_over

    def reset(self):
        return
