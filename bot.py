# import json

# import nltk
# import numpy as np
# from flask import Flask, jsonify, render_template, request
# from nltk.stem import WordNetLemmatizer
# from pymongo import MongoClient
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression

# app=Flask(__name__)

# client =MongoClient('mongodb://localhost:27017')
# app.config['SECRET_KEY']='thisissecret'
# db = client['bot']
# user = db['bot1']
# # print(json_coll)

# # Load and preprocess the training data
# with open('C:/Users/aman singh/OneDrive/Desktop/chat2bot/json/data.json') as file:
#     data = json.load(file)

# lemmatizer = WordNetLemmatizer()
# tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# patterns = []
# tags = []

# for intent in data['intents']:
#     for example in intent['patterns']:
#         tokens = nltk.word_tokenize(example)
#         tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
#         patterns.append(' '.join(tokens))
#         tags.append(intent['tag'])

# patterns = tfidf_vectorizer.fit_transform(patterns)
# tags = np.array(tags)

# # Train a machine
# train_m = LogisticRegression(max_iter=1000)
# train_m.fit(patterns, tags)

# #function for processing and generating responses
# def preprocess_input(text):
#     tokens = nltk.word_tokenize(text)
#     tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
#     return ' '.join(tokens)

# def predict_intent(text):
#     X_test = tfidf_vectorizer.transform([text])
#     y_pred = train_m.predict(X_test)
#     return y_pred[0]

# def generate_response(intent):
#     for item in data['intents']:
#         if item['tag'] == intent:
#             responses = item['responses']
#             return np.random.choice(responses)

# # Implement a loop to take input and generate responses


# def chatbot_response(userText):
#     preprocessed_input = preprocess_input(userText)
#     intent = predict_intent(preprocessed_input)
#     res = generate_response(intent)
#     return res
    





# app.static_folder = 'static'
# @app.route("/")

# def home():
#     return render_template("index.html")
# @app.route("/get")
# def get_bot_response():
    
        
#     userText = request.args.get('msg')
#     return chatbot_response(userText)
# if __name__ == "__main__":
#     app.run()
