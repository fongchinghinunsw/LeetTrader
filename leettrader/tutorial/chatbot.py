import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
import pickle
import json
import random
from flask import Blueprint, jsonify
chatbot = Blueprint('chabot', __name__)

from keras.models import load_model
model = load_model('leettrader/tutorial/model.h5')
intents = json.loads(open('leettrader/tutorial/intents.json').read())
words = pickle.load(open('leettrader/tutorial/words.pkl','rb'))
classes = pickle.load(open('leettrader/tutorial/classes.pkl','rb'))


def clean_up_user_input(sentence):
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words

def get_bag_of_words(sentence, words):
  sentence_words = clean_up_user_input(sentence)
  bag = [0] * len(words)
  for s in sentence_words:
    for i, word in enumerate(words):
      if word == s:
        bag[i] = 1

  return np.array(bag)

def predict_class(sentence):
    # filter below  threshold predictions
    p = get_bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        print(str(r[1]))
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    if return_list == []:
      return_list.append({"intent": 'noanswer', "probability": str(1)})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

@chatbot.route('/askQuestion/<string:user_input>', methods=['GET', 'POST'])
def askQuestion(user_input):
  intent = predict_class(user_input)
  response = getResponse(intent, intents)
  return jsonify(response=response), 200

