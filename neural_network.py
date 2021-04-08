import random as rand
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


class NeuralNetworkLoader:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open("intents.json").read())

        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_letters = ['.', ',', '?', '!']

    def updateNeuralNetwork(self):
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                words_list = nltk.word_tokenize(pattern)
                self.words.extend(words_list)
                self.documents.append((words_list, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        words = [self.lemmatizer.lemmatize(word.lower()) for word in self.words if word not in self.ignore_letters]
        words = sorted(set(words))
        classes = sorted(set(self.classes))

        pickle.dump(words, open("words.pkl", 'wb'))
        pickle.dump(classes, open("classes.pkl", 'wb'))

        training = []
        output_empty = np.zeros(len(classes))

        for document in self.documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(document[1])] = 1
            training.append((bag, output_row))

        rand.shuffle(training)
        training = np.array(training)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save("chatbotmodel.h5", hist)
        print("Updating Neural Network - Done")


# Runner = NeuralNetworkLoader()
# Runner.updateNeuralNetwork()

