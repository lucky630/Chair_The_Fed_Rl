import json
import torch
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

torch.manual_seed(1)

##used to define the state.

class STATE(object):
    
    ##json file for saving and loading the news and its labels
    news_dic_loc='C:\\Users\\royal\\Downloads\\Compressed\\DeepGamingAI_FIFARL-master\\record'+'\\'+'new_dic.json'

    ##128 dimension features for the state.
    def get_features_128(self,news,fed,unemp,infla):
        print('\n features 128 method\n')
        news_lab = self.tfidf(news)
        embeds = torch.nn.Embedding(64, 125)
        look_tor= torch.tensor([news_lab],dtype=torch.long)
        tor_embed = embeds(look_tor)
        numpy_embed = tor_embed.data.numpy().reshape(-1,125)
        fina_embed = np.append(numpy_embed,[fed,unemp,infla]).reshape(-1,128)
        norm1 = fina_embed / np.linalg.norm(fina_embed)
        print(norm1)
        return norm1

    ##4 dimension features for the state.
    def get_features_4(self,news,fed,unemp,infla):
        print('\n features 4 method\n')
        news_lab = self.tfidf(news)
        #x = np.array([self.word_to_ix[news],fed,unemp,infla],dtype=np.float).reshape(-1,4)
        x = np.array([news_lab,fed,unemp,infla],dtype=np.float).reshape(-1,4)
        norm1 = x / np.linalg.norm(x)
        print("state is: "+str(norm1))
        return norm1

    def tfidf(self,news):
        print('\n tfidf transform method\n')
        vectorizer = CountVectorizer()
        tfidf_vectorizer = TfidfTransformer(norm='l2')
        new_to_ix = {}
        with open(self.news_dic_loc,'r') as fp:
            new_to_ix=json.load(fp)
        x = list(new_to_ix.keys())
        tfidf_matrix_new = tfidf_vectorizer.fit_transform(vectorizer.fit_transform(list(new_to_ix.keys())))
        ls=[]
        ls.append(news)
        tfidf_test = tfidf_vectorizer.transform(vectorizer.transform(ls))
        k =cosine_similarity(tfidf_test[0], tfidf_matrix_new)
        elmnt = np.partition(k.flatten(), -2)[-2]
        if(elmnt>0.5):
            print('found similar news')
            itemindex = np.where(k==elmnt)
            lab = new_to_ix[x[itemindex[1][0]]]
        else:
            print('found new news')
            lab = len(new_to_ix)+1
            new_to_ix[news]=lab
            with open(self.news_dic_loc,'w') as fp:
                json.dump(new_to_ix,fp)
        return lab
