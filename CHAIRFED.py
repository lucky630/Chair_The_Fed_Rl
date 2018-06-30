import numpy as np
import pytesseract as pt
from STATE import STATE
from Game_util_selenium import *
from selenium import webdriver
import time

class CHAIRFED(object):
	
    state_graph = STATE()
    reward = 0

    def __init__(self):
        self.reset()

    def _get_reward(self, driver):
        print('\n get reward method\n')
        screen = screen_grab(driver)
        ingame_reward=-10
        try:
            fed=float(''.join(get_fed_rates(screen).split()).split('%')[0])
            unemp=float(''.join(get_unemploy_rate(screen).split()).split('%')[0])
            infl=float(''.join(get_inflate_rate(screen).split()).split('%')[0])
            if (unemp > 4.0 and unemp < 6.0) and (infl > 1.0 and infl < 3.0):
                ingame_reward = 1
            else:
                ingame_reward = -1
            print('q-learning reward: ' + str(ingame_reward))
        except ValueError:
            print('Value Exception in get_reward method: ')
        return ingame_reward

    def _is_over(self,driver):
        print('\n is_over method\n')
        is_over=False
        st = get_last_msg(driver)
        if st == 'Congratulations!' or st=='Sorry.':
            is_over = True
            print('last quarter result is :'+st)
        else:
            is_over = False
        #is_over = True if action in [0, 1, 2, 3, 4, 5, 6, 7] else False
        return is_over

    def observe(self,driver):
        print('\n observe method\n')
        # get current state s from screen using screen_grab
        screen = screen_grab(driver)
        fed,unemp,infl,news=0.0,0.0,0.0,''
        try:
            fed=float(''.join(get_fed_rates(screen).split()).split('%')[0])
            unemp=float(''.join(get_unemploy_rate(screen).split()).split('%')[0])
            infl=float(''.join(get_inflate_rate(screen).split()).split('%')[0])
            news=' '.join(get_news(screen).split('\n'))
            data=str(fed)+','+str(unemp)+','+str(infl)+','+news
            print(data.encode('utf8'))
            # process through state_graph to get the state.
            #state = self.state_graph.get_features_128(news,fed,unemp,infl)
        except ValueError:
            print('Value Exception in observe method: ')
        state = self.state_graph.get_features_4(news,fed,unemp,infl)
        return state

    def act(self, action, driver):
        print('\n act method\n')
        display_action = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        print('action: ' + str(display_action[action]))
        screen = screen_grab(driver)
        
        fed=float(''.join(get_fed_rates(screen).split()).split('%')[0])
        set_fed_rate(driver,fed,display_action[action])

        game_over = self._is_over(driver)
        reward = self._get_reward(driver)
        ##condition for delay in finish page loading..
        if reward==-10:
            print('game over true bcz of value exception. wait for 5 second:')
            time.sleep(5)
            game_over = self._is_over(driver)
            reward = self._get_reward(driver)
        return self.observe(driver), reward, game_over

    def reset(self):
        return
