
# from urllib.parse import quote_from_bytes
import os
import json
from  requests import get
from bs4 import BeautifulSoup
import nltk
from socket import *
import numpy as np
from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
# from requests import get 
import requests

from werkzeug.utils import secure_filename

# import wikipedia
from googlesearch import search
# import time
# from googlesearch.googlesearch import search

lemmatizer = WordNetLemmatizer()
app = Flask(__name__)
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

    # text = "Your string"
    text_bytes = text.encode('utf-8')  # Convert string to bytes

# Use the bytes object with quote_from_bytes()
    # encoded_text = quote_from_bytes(text_bytes)

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


# def perform_google_search(userText):
    # search_results = []
    # # google_search = requests.get("https://www.google.com/search?q=" + userText)

    # google_search = requests.get("https://www.google.com/search?q=abcd&sxsrf=APwXEdcvXDTQ3mPaOtuOrE3cQXMJT2uQpA%3A1682601521037&source=hp&ei=MHZKZMfuPNmp2roPlvKquAs&iflsig=AOEireoAAAAAZEqEQaIZgcz-h3Gk58rQcaK7GbTETRJ6&ved=0ahUKEwjHxtSPk8r-AhXZlFYBHRa5CrcQ4dUDCBE&oq=abcd&gs_lcp=Cgdnd3Mtd2l6EAxQAFgAYABoAHAAeACAAQCIAQCSAQCYAQA&sclient=gws-wiz")

    
    # # print(google_search.text)
    # soup = BeautifulSoup(google_search.text, 'html.parser')
    # print(soup)
    # search_results = soup.find_all('p')

    
    # Extract the URLs from the search results
    # search_urls = [result['href'] for result in search_results]
    # return search_urls

# def perform_google_search(userText):
    # search_results = []
    # query = "https://www.bing.com/ " + userText
    # for result in search(query, num=5, stop=5, lang='en'):
    #     search_results.append(result)
    # return search_results

def perform_google_search(userText):
    search_results = []
    query = userText
    for result in search(query,tld="co.in" ,num=5, stop=5,lang='en',  ):  #lang='hi'' or
        search_results.append(result)
    # print(search_results)
    paragraph_content = []
    
    for url in search_results:
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')

        for paragraph in paragraphs:
            paragraph_content.append(paragraph.text)
    
    return "".join(paragraph_content)


# def perform_google_search(userText):
#     search_results = []
#     query = userText
#     try:
#         for result in search(query, tld="co.in", num=5, stop=5, lang='en'):
#             search_results.append(result)
        
#         paragraph_content = []
#         for url in search_results:
#             try:
#                 response = requests.get(url)
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 paragraphs = soup.find_all('p', string=True)

#                 for paragraph in paragraphs:
#                     paragraph_content.append(paragraph.text)
#             except Exception as e:
#                 print(f"Error occurred while scraping URL: {url}")
#                 print(e)
        
#         return "".join(paragraph_content)
#     except Exception as e:
#         print("Error occurred during the Google search.")
#         print(e)
#         return ""





# Implement a loop to take input and generate responses

def chatbot_response(userText):
    preprocessed_input = preprocess_input(userText)
    # intent = predict_intent(preprocessed_input)

    if userText in question:
        intent = predict_intent(preprocessed_input)
        res = generate_response(intent)
        # print('response')
        return res
        # print(res)
    else:
        google_results = perform_google_search(userText)
        # print("WRGFETGTRSRHYRJHRE",google_results)
        if google_results:

            return "Here are some search results: \n  \t"  + "".join(google_results)
        
        else:
            return "I'm sorry, I couldn't find any information."

    # else:
    #     return generate_response(intent)
    
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")




# def chatbot_response(userText):
#     preprocessed_input = preprocess_input(userText)
#     intent = predict_intent(preprocessed_input)
#     res = generate_response(intent)  
#     return res
 
app.static_folder = 'static'

################ for open file ####################

# @app.route("/", methods=['POST', 'GET'])
# def upload():
#     user_text = request.args.get('msg')
#     if user_text == 'i want upload a file':
#         return redirect("/uploader")
    # else:
    #     return chatbot_response(user_text)
    
# @app.route("/uploader")
# def uploader():
#     return render_template("upload_file.html")
 

##############################################################


# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/uploader")
# def uploader():
#     return render_template("upload_file.html")

###############  here get response ################################
# @app.route("/get", methods=['GET'])
# def get():
#     userText = request.args.get('msg')

#     # user_text = request.args.get('msg')
#     a='i want upload a file'
#     b='I want to upload a file.'
#     c='i want to upload a file'
#     d='I want upload a file.'
#     if userText == a or userText == b or userText == c or userText == d :
#         return redirect("/upload_file")
#     collection.insert_one({'usertext':userText})
#     print(userText)
#     return chatbot_response(userText)

# @app.route("/upload_file")
# def upload_file():
#     return render_template("upload_file.html" , message="i want upload a file")
#######################################################################################

############################# here upload file ########################################
# @app.route("/upload_file" , methods=['POST','GET'])
# def upload_file():
#     if request.method=='POST':
#         f= request.files['file'] 
#         print(f)
#         file_doc = {
#             'filename': f.filename
#             }
#         db['files'].insert_one(file_doc)

#         f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
#         # f.save("/uploaded_file" + f.filename) 
#         print(f)
        
#         return 'uploaded_file  successfully '
#     return render_template("upload_file.html" ,message="I want to upload a file.")    ## , message="i want upload a file"
###########################################################################################

# @app.route('/submit', methods=['GET'])
# def submit():
#     message_text = request.args.get('messageText')
#     collection.insert_one({'usertext': message_text})
#     print(message_text)  # Print the message text for debugging
#     return chatbot_response(message_text)  # Return a response indicating successful processing

# def upload_file():
#         f = request.files['file']
#         msg= request.form['msg']
#         file_url = 'https://mpagapi.mpulsenet.com/csv_upload'  
#         # files = {'file': f, 'msg':msg}
#         # f.save(file_url)
#         files = {
#             'uploadFile': (f.filename, f, 'text/csv'),
#         } 
#         boddy={
#             'uploadfor': 'outage_check_CP_DA0019BA'
#         }

#         print('kfehugyuewhjkengkieugiej',files)
#         # print('kndjbud',files)
#         response = requests.post(file_url, files=files,data=boddy)
#         print(response)
        
#         if response.status_code == 200 or response.status_code == 201:
#             # return 'File uploaded successfully!'+str(response.json())
#             # response_data = json.dumps(response.json()) 
#             response_data = response.json() 
#             if response_data:
#                 return response_data
#                 # return redirect('/') 
#                 # return render_template("upload_file.html", message="I want to upload a file." )
#                 # return render_template("show_resp.html", message="File uploaded successfully!", response=response_data )
#         else:          
#             return 'File upload failed.'




@app.route("/get", methods=['GET'])
def get():
    userText = request.args.get('msg')

    # a = 'i want upload a file'
    # b = 'I want to upload a file.'
    # c = 'i want to upload a file'
    # d = 'I want upload a file.'
    
    # if userText == a or userText == b or userText == c or userText == d:   ##.lower() in [a, b, c, d]:
    #     return redirect("/upload_file")
     
        # return render_template("upload_file.html", message=userText, chatbot_response=None) 
    collection.insert_one({'usertext': userText})

        # response = chatbot_response(userText)
    # response_data = response.json() 
    # if response_data:
    #     return response_data
    
    return chatbot_response(userText)
    # return render_template("index.html", message=userText, chatbot_response=response)
    
    

@app.route("/upload_file", methods=['POST',"GET"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        msg= request.form['msg']
        file_url = 'https://mpagapi.mpulsenet.com/csv_upload'  
        # files = {'file': f, 'msg':msg}
        # f.save(file_url)
        files = {
            'uploadFile': (f.filename, f, 'text/csv'),
        } 
        boddy={
            'uploadfor': 'outage_check_CP_DA0019BA'
        }

        print('kfehugyuewhjkengkieugiej',files)
        # print('kndjbud',files)
        response = requests.post(file_url, files=files,data=boddy)
        print(response)
        
        if response.status_code == 200 or response.status_code == 201:
            # return 'File uploaded successfully!'+str(response.json())
            # response_data = json.dumps(response.json()) 

            response_data = response.json() 
            
            if response_data:
                return response_data
                # return chatbot_response(response_data)
                # return response() 
                # return render_template("upload_file.html", message="I want to upload a file." )
                # return render_template("show_resp.html", message="File uploaded successfully!", response=response_data )
        else:          
            return 'File upload failed.'

    return render_template("upload_file.html", message="I want to upload a file." )

 
if __name__ == "__main__":
    app.run(debug=True)

