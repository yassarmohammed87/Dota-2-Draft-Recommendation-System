import numpy as np
import pandas as pd
import requests
import json
import urllib
import tensorflow as tf
import tensorflow_datasets
from tensorflow import keras
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import Word2Vec

def preds(arr):
    
    data=np.reshape(arr,(1,arr.shape[0],arr.shape[1]))
    data=tf.data.Dataset.from_tensor_slices(data)
    data=data.map(lambda x: x[:-1])
    data=data.batch(1,drop_remainder=True)
    return data



def predictions(arr):
    picks_inds=[4,5,6,7,12,13,14,15,22]
    model=keras.models.load_model('Models\\lstm128_30topk.h5')
    embed_df=pd.read_csv('modified_hero_to_embedding.csv',index_col='Heroes')
    hero_df=pd.read_csv('hero_df.csv')
    id_arr=[]
    for i in arr:
        id_arr.append(hero_df.loc[hero_df['localized_name']==i]['sid'].values)
    instance=[]
    # label=embed_df.loc[arr].index[-1]
    for i in embed_df.loc[arr[picks_inds]].index:
        instance.append(embed_df.loc[i][embed_df.columns].values)
    
    
    instance=np.array(instance)
    instance=preds(instance)


    predictions=model.predict(instance)
    inbans=0
    # even_ind=[True,False,True,False,True,False,True,False,True,False,True,False,True,False]
    modified_pred=np.copy(predictions)
    for i,j in enumerate(modified_pred):
        answers=np.argsort(-j)[:3]
        while np.intersect1d(answers,id_arr).shape[0]!=0:
            intersection=np.intersect1d(answers,id_arr)
            modified_pred[i,intersection]=-10.0
            answers=np.argsort(-modified_pred[i])[:3]

    ind=np.argsort(-modified_pred[0])[:3]
    
    return ind