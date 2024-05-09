# %%
import os
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import sys

import json
with open('intents.json', 'r') as file:
    data = json.load(file)
intents = data['intents']


# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x = vectorizer.fit_transform(patterns)
y = tags

counter = 0

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

import pathlib
import textwrap
import google.generativeai as genai
#from google.colab import userdata
from IPython.display import display
from IPython.display import Markdown

# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, ">", predicate=lambda _: True))

api = 'AIzaSyCPTrN4irJspGsFB9vVdeEPQAAiiPmisis'
genai.configure(api_key=api)

import os
os.environ[api] = 'AIzaSyCPTrN4irJspGsFB9vVdeEPQAAiiPmisis'

model = genai.GenerativeModel('models/gemini-1.0-pro-latest')

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response
        
def is_topic_specific(response):
    keywords = ["stress", "panic","anxiety","sleep","mental health",'anxious','fearful','nervous','worried','money','financial','social','failure','breakup']
    response_text = response.text.lower()
    for keyword in keywords:
        if keyword in response_text:
            return True
    return False

def get_gemini_response(user_input):
    response = model.generate_content(user_input)
    if is_topic_specific(response):
        return response
    else:
        return "I'm sorry! I cannot answer that! I am designed to talk about your mental health issues!"
#print(get_gemini_response("headache"+"keep the answer short and to the point. Only suggest the preventions"))

# Function to handle user input and send a response
# def process_input(input_text):
    # response = "Processed: " + input_text
    #print(response)

# for line in sys.stdin:
#     input_text = line.strip()
#     process_input(input_text)

if len(sys.argv) == 2:
    for arg in sys.argv[1:]:
        response_text = chatbot(arg)
        print(response_text)
elif len(sys.argv) == 3:
    print("what problem are you facing?('exit' to quit):")
    #user_input = input("What problems are you facing? (type 'exit' to quit): ")
    user_input = sys.argv[2]
    response_text = get_gemini_response(user_input+" keep the answer short and to the point. Only suggest the preventions")
    print(response_text)
    print("is there anything else i can do for you")
    #print(response_text + "\n\nIs there anything else I can help you with?")
else:
    while True:
        print("what problem are you facing?(type 'exit' to quit):")
        #user_input = input("What problems are you facing? (type 'exit' to quit): ")
        user_input = sys.argv[1]
        if user_input.lower() == 'exit':
            break
        response_text = chatbot(user_input)
        print(response_text + '\n\nIs there anything else I can help you with?')

# if len(sys.argv) > 1:
#     input_text = ' '.join(sys.argv[1:])
#     process_input(input_text)
# else:
#     print("No input provided.")

# while True:
#     #user_input = input("What problems are you facing? (type 'exit' to quit): ")
#     user_input = input()
#     # print("userinput", user_input)
#     if user_input.lower() == 'exit':
#         break
#     response_text = get_gemini_response(user_input+" keep the answer short and to the point. Only suggest the preventions")
#     print(response_text + '\n\nIs there anything else I can help you with?')
#     input_text = ''

# %%



