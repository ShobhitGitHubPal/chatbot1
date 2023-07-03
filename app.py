
# from urllib.parse import quote_from_bytes
import os
import json
from  requests import get
from bs4 import BeautifulSoup
import nltk
from socket import *
import numpy as np
from flask import Flask, session, jsonify, render_template, request, make_response, redirect, url_for
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
# from requests import get 
import requests
# from flask_session import Session
from werkzeug.utils import secure_filename
from datetime import datetime
import datetime

# import wikipedia
from googlesearch import search
# import time
# from googlesearch.googlesearch import search


lemmatizer = WordNetLemmatizer()
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

app.config['UPLOAD_FOLDER'] = 'uploaded'
# file=os.path.join(os.getcwd(),'uploaded_file')
# print(file,"files")
# app.config['UPLOAD_FOLDER'] = file

client =MongoClient('mongodb://localhost:27017')
app.config['SECRET_KEY']='thisissecret'
db = client['bot']
collection = db['data2']
collection2 = db['files']
# userText=[]

with open("C:/Users/hp pc/OneDrive/Desktop/dchat/data.json") as file:
        data = json.load(file) 

lemmatizer = WordNetLemmatizer()
# tfidf_vectorizer = TfidfVectorizer(stop_words='english')
question = []
tags = []

for intent in data['intents']:
    for example in intent['patterns']:
        tokens = nltk.word_tokenize(example)
        tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
        question.append(' '.join(tokens))
        tags.append(intent['tag'])
tfidf_vectorizer = TfidfVectorizer(stop_words='english')#
patterns = tfidf_vectorizer.fit_transform(question)
tags = np.array(tags)

# Train a machine
train_m = LogisticRegression(max_iter=1000)
train_m.fit(patterns, tags)

# function for processing and generating responses
def preprocess_input(text):
    # text= text.decode('utf-8')
    text = str(text)

    # bytes_value = text.encode('utf-8')  # Convert string to bytes
    # quote_from_bytes(bytes_value)
    text_bytes = text.encode('utf-8')  # Convert string to bytes

    tokens = nltk.word_tokenize(text)
    # tokens = nltk.TreebankWordTokenizer(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
    return ''.join(tokens)



def predict_intent(text):
    X_test = tfidf_vectorizer.transform([text])
    y_pred = train_m.predict(X_test)
    return y_pred[0]

def generate_response(intent):
    for item in data['intents']:
        if item['tag'] == intent:
            responses = item['responses']
            return np.random.choice(responses)




def perform_google_search(userText):
    search_results = []
    query = userText
    for result in search(query,tld="co.in" ,num=5, stop=5,lang='en',  ):  #lang='hi'' or
        search_results.append(result)
    # print(search_results)
    paragraph_content = []
    session['upload_response'] = paragraph_content
    num_lines = 5  # Number of important lines to display
    for url in search_results:
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')

        lines_displayed = 0 #
        for paragraph in paragraphs:
            # lines= paragraph.text.lower()
            # for line in lines:
            #     if line:
            #         paragraph_content.append(line)
            #         lines_displayed += 1
            #         if lines_displayed == num_lines:
            #             break
            # if lines_displayed == num_lines:
            #     break

            lines = paragraph.text.split('. ')#
            for line in lines:#
                if line.strip() != '':#
                    paragraph_content.append(line.strip())#
                    lines_displayed += 1#
                    if lines_displayed == num_lines:#
                        break#
            if lines_displayed == num_lines:#
                break#

            # paragraph_content.append(paragraph.text)
            
    
    return "".join(paragraph_content)

        
   
    
app.static_folder = 'static'

# @app.route("/")
# def home(): 
    
#     return render_template("index.html")


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     # ...
#     return render_template("index.html")


@app.route("/", methods=['GET', 'POST'])
def home():
    DateTime = None
    if 'upload_response' in session:
        # session['upload_file'] = session['upload_file']  # Update to store the filename instead of the function reference
        # session.pop('upload_file', None)  # Use the string 'upload_file' as the key
        filename =session['upload_file'] # Update to store the filename instead of the function reference
        session.pop('upload_file', None)
        
        response = session['upload_response']

        # for response in session['upload_response']:
        # return

        session.pop('upload_response', None)
          # Remove the session variable after retrieving its value
        current_time = datetime.datetime.now().time()
        formatted_time = current_time.strftime("%H:%M")
        print(formatted_time)
        return render_template("index.html", formatted_time=formatted_time, response=response, filename=filename)
    return render_template("index.html")

# Implement a loop to take input and generate responses
# data = ['i want upload a file' or 'I want upload a file.']

def chatbot_response(userText):
    preprocessed_input = preprocess_input(userText)
    # intent = predict_intent(preprocessed_input)

    if userText in question:
        intent = predict_intent(preprocessed_input)
        res = generate_response(intent)
        # session['upload_response'] = res
        return res
        
    else: 
        google_results = perform_google_search(userText)
        # print("WRGFETGTRSRHYRJHRE",google_results)
        if google_results:
            return "Here are some search results: \n  \t"  + "".join(google_results)
        
        else:
            return "I'm sorry, I couldn't find any information."
    
@app.route("/upload", methods=['POST',"GET"])
def upload_file():   
    if request.method== 'POST':
        # if 'file' not in request.files:
        #     return "No file part in the request"
        f = request.files['file']
        print(f)
        if not file:
            print('file not')
            # return jsonify({'message': 'No file selected'})

        # msg= request.form.get('msg')
        file_url = 'https://mpagapi.mpulsenet.com/csv_upload'  
        
        files = {
            'uploadFile': (f.filename, f, 'text/csv'),
        } 
        boddy={
            'uploadfor': 'outage_check_CP_DA0019BA'
        }
        session['upload_file'] = f.filename

        print('kfehugyuewhjkengkieugiej',files)
        # print('kndjbud',files)
        response = requests.post(file_url, files=files,data=boddy)
        print(response)
        
        if response.status_code == 200 or response.status_code == 201:
            # return 'File uploaded successfully!'+str(response.json())
            response_data = json.dumps(response.json()) 
            # response = []
            # response_data.append(response)
            session['upload_response'] = response_data
            
            return redirect('/')
        else:
            session['upload_response'] = 'File upload failed.'

    return render_template("upload_file.html" ,message="I want to upload a file." )

@app.route("/get", methods=['GET','POST'])
def get():
    userText = request.args.get('msg')
    collection.insert_one({'usertext': userText})
    if userText == 'i want upload a file' :
        return redirect('upload')
    # bot_response = chatbot_response(userText)
    # return bot_response
    return chatbot_response(userText)
 
if __name__ == "__main__":
    app.run(debug=True, port=2020)






# lines = paragraph.text.split('. ')#
            # for line in lines:#
            #     if line.strip() != '':#
            #         paragraph_content.append(line.strip())#
            #         lines_displayed += 1#
            #         if lines_displayed == num_lines:#
            #             break#
            # if lines_displayed == num_lines:#
            #     break#

            # paragraph_content.append(paragraph.text)