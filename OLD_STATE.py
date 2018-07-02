import json
import torch
import os
import numpy as np

torch.manual_seed(1)

##used to define the state.

class STATE(object):
    word_to_ix={}
    news_ll=[]
    ##json file for saving the loading the news and its unique position
    news_dic_loc='C:\\Users\\royal\\Downloads\\Compressed\\DeepGamingAI_FIFARL-master\\record'+'\\'+'news_dic.json'
    news_list_loc='C:\\Users\\royal\\Downloads\\Compressed\\DeepGamingAI_FIFARL-master\\record'+'\\'+'news_list.json'

    ##load the word_to_ix which contain news and its unique index and news_ll contain unique news.
    def __init__(self):
        
        with open(self.news_dic_loc,'r') as fp:
            self.word_to_ix=json.load(fp)
        with open(self.news_list_loc,'r') as fp:
            self.news_ll=json.load(fp)

    ##128 dimension features for the state.
    def get_features_128(self,news,fed,unemp,infla):
        print('\n features 128 method\n')
        word_to_ix=self.word_to_ix
        news_ll=self.news_ll
        if news not in news_ll:
            word_to_ix[news]=len(set(news_ll))
            news_ll.append(news)
            with open(self.news_dic_loc,'w') as fp:
                json.dump(word_to_ix,fp)
            with open(self.news_list_loc,'w') as fp:
                json.dump(news_ll,fp)
        embeds = torch.nn.Embedding(len(word_to_ix), 125)
        look_tor= torch.tensor([word_to_ix[news]],dtype=torch.long)
        tor_embed = embeds(look_tor)
        numpy_embed = tor_embed.data.numpy().reshape(-1,125)
        fina_embed = np.append(numpy_embed,[fed,unemp,infla])
        return fina_embed.reshape(-1,128)

    ##4 dimension features for the state.
    def get_features_4(self,news,fed,unemp,infla):
        print('\n features 4 method\n')
        if news not in self.news_ll:
            self.word_to_ix[news]=len(set(self.news_ll))
            self.news_ll.append(news)
            with open(self.news_dic_loc,'w') as fp:
                json.dump(self.word_to_ix,fp)
            with open(self.news_list_loc,'w') as fp:
                json.dump(self.news_ll,fp)
        return np.array([self.word_to_ix[news],fed,unemp,infla],dtype=np.float).reshape(-1,4)
