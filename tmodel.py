# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:05:58 2021

@author: HP
"""

import numpy
import tflearn
import json
import random
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

def load_data():
    global data
    global words
    global labels
    global training
    global output    
    with open("./intents.json") as file:
        data = json.load(file)

    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

def load_model():
    global model
    from tensorflow.python.framework import ops
    ops.reset_default_graph()

    net = tflearn.input_data(shape=[None,len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)
    
    model = tflearn.DNN(net)
    model.load("model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def chat(command):
    inp = command
    inp = inp.lower()
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
        
    if results[results_index] > 0.6:
        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]
             
        return random.choice(responses)       
    else:
        return "Sorry!! I didn't get that. Could you please repeat or ask something else?"
    