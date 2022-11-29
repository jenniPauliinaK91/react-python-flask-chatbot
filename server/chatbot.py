#OmaChatti.py
#Käyttää OmaChatti_model.h5 -neural network mallia, jonka perusteella poimitaan vastauksia
#chatin keskustelussa
import enum
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from flask import Flask, request 
from flask_cors import CORS
#otetaan sanojen perusmuodon muokkaus ja json-tiedosto käyttöön, sanat, luokat ja NeuralNW -malli
lemmatizer=WordNetLemmatizer()
intents=json.loads(open('server/intents.json').read())
words=pickle.load(open('./words.pkl','rb'))
classes=pickle.load(open('./classes.pkl','rb'))
model=load_model('./OmaChatti_model.h5')


#app.run()
# #funktiot, joilla vastaus poimitaan
def bag_of_words(lause):
    #tekee listan lauseen eri sanoista, jotta voidaan sanojen perusteella laskea todennäköisyyksiä
    lauseen_sanat=nltk.word_tokenize(lause)
    lauseen_sanat=[lemmatizer.lemmatize(word) for word in lauseen_sanat]
    bag=[0] * len(words)
    for w in lauseen_sanat:
        for i, word in enumerate(words):
            if word==w:
                bag[i]=1
    return np.array(bag)

def predict_class(lause):
    #hakee tilastollisen todennäköisyyden perusteella todennäköisimmän vastausvaihtoehdon
    bow=bag_of_words(lause)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25
    results=[[i,r] for i, r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list=[]
    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    #hakee vastauksen tilastollisen ennakoinnin perusteella. Vastaus haetaan json-tiedostosta
    #predict_class -funktion poimiman korkeimman todennäköisyyden perusteella.
    tag=intents_list[0]['intent']
    list_of_intents=intents_json['intents']
    for i in list_of_intents:
        if i['tag']==tag:
            result=random.choice(i['responses'])
            break
    return result

def chatbotVastaus(msg):
    ints=predict_class(msg)
    vastaus=get_response(ints,intents)
    return vastaus



#FLASK 
from flask import Flask, request 
app=Flask(__name__)
CORS(app)
@app.route("/getReply", methods=['POST'])
def HaeVastaus():
    jsonPost=request.json
    data=jsonPost['msg'] #haetaan frontin post-requestista käyttäjän kysymys
    return str(chatbotVastaus(data)) #palautetaan chattibotin vastaus string-muodossa

app.run()




#  BOTIN TESTAAMISEEN ILMAN FRONTENDIA:

# def get_response(intents_list, intents_json):
#     tag=intents_list[0]['intent']
#     list_of_intents=intents_json['intents']
#     for i in list_of_intents:
#         if i['tag']==tag:
#             result=random.choice(i['responses'])
#             break
#     return result

# print("Discuss: ")
# while True:
#     kysymys=input('You: ')
#     ints=predict_class(kysymys)
#     vastaus=get_response(ints,intents)
#     print("Bot: " + vastaus)
