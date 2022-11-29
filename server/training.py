#training.py
#Luodaan json-datasta neural network malli. Luodaan sanoista data, joka muunnetaan numeeriseksi.
from abc import ABCMeta, abstractmethod
import random
import json
import pickle
from re import S
import numpy as np
import os
import nltk


from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.models import load_model
from tensorflow.python.eager.context import DEVICE_PLACEMENT_SILENT_FOR_INT32

#nltk ja json osat käyttöön
nltk.download('punkt',quiet=True)
nltk.download('wordnet',quiet=True)
lemmatizer=WordNetLemmatizer()
intents=json.loads(open('server/intents.json').read())

#aluksi jokainen sana erikseen (tokenize)
words=[]
classes=[]
documents=[]
ignore_letters=['!','?','.',',',':']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word=nltk.word_tokenize(pattern)
        words.extend(word)
        documents.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
#print(documents)

#sanojen perusmuodot yms
words=[lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words=sorted(list(set(words)))
classes=sorted(list(set(classes)))


#tallennetaan sanat ja luokat
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

#luodaan training data
training=[]
output_empty=[0] * len(classes)
for doc in documents:
    bag=[]
    word_patterns=doc[0]
    word_patterns=[lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row=list(output_empty)
    output_row[classes.index(doc[1])]=1
    training.append([bag,output_row])
#sekoitetaan ja luodaan numpy taulukko
random.shuffle(training)
training=np.array(training)
train_x=list(training[:,0])
train_y=list(training[:,1])


#luodaan Neural Network model
model=Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))
#luodaan malli
sgd=SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#Mallin training ja tallennus
hist=model.fit(np.array(train_x),np.array(train_y),epochs=200, batch_size=5, verbose=1)
model.save('OmaChatti_model.h5', hist)
print("Malli on luotu!")
