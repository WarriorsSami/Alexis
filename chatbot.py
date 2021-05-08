import random as rand
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model
import tensorflow as tf


class ConversationMode:
    def __init__(self):
        tf.compat.v1.enable_eager_execution()
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open("intents.json").read())

        self.words = pickle.load(open("words.pkl", 'rb'))
        self.classes = pickle.load(open("classes.pkl", 'rb'))
        self.model = load_model("chatbotmodel.h5")

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = np.zeros(len(self.words))
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if w == word:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [(i, r) for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)

        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, intent):
        tag = intent[0]['intent']
        list_of_intents = self.intents['intents']
        result = ""
        for category in list_of_intents:
            if category['tag'] == tag:
                result = rand.choice(category['responses'])
                break
        return result

    def test(self):
        print("Conversation mode is on!")
        while True:
            message = input()
            intent = self.predict_class(message)
            response = self.get_response(intent)
            print(response)

# Debugger = ConversationMode()
# Debugger.test()
