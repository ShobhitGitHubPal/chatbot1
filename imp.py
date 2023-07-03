'''
def perform_google_search(userText):
    search_results = []
    query = userText
    try:
        for result in search(query, tld="co.in", num=5, stop=5, lang='en'):
            search_results.append(result)
        
        paragraph_content = []
        for url in search_results:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p', string=True)

                for paragraph in paragraphs:
                    paragraph_content.append(paragraph.text)
            except Exception as e:
                print(f"Error occurred while scraping URL: {url}")
                print(e)
        
        return "".join(paragraph_content)
    except Exception as e:
        print("Error occurred during the Google search.")
        print(e)
        return ""

'''




'''

############### for open file ####################

@app.route("/", methods=['POST', 'GET'])
def upload():
    user_text = request.args.get('msg')
    if user_text == 'i want upload a file':
        return redirect("/uploader")
    else:
        return chatbot_response(user_text)
    
@app.route("/uploader")
def uploader():
    return render_template("upload_file.html")
 

#############################################################


##############  here get resoonse ################################
@app.route("/get", methods=['GET'])
def get():
    userText = request.args.get('msg')

    # user_text = request.args.get('msg')
    a='i want upload a file'
    b='I want to upload a file.'
    c='i want to upload a file'
    d='I want upload a file.'
    if userText == a or userText == b or userText == c or userText == d :
        return redirect("/upload_file")
    collection.insert_one({'usertext':userText})
    print(userText)
    return chatbot_response(userText)

@app.route("/upload_file")
def upload_file():
    return render_template("upload_file.html" , message="i want upload a file")
######################################################################################

############################ here upload file ########################################
@app.route("/upload_file" , methods=['POST','GET'])
def upload_file():
    if request.method=='POST':
        f= request.files['file'] 
        print(f)
        file_doc = {
            'filename': f.filename
            }
        db['files'].insert_one(file_doc)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        # f.save("/uploaded_file" + f.filename) 
        print(f)
        
        return 'uploaded_file  successfully '
    return render_template("upload_file.html" ,message="I want to upload a file.")    ## , message="i want upload a file"
#########################################################################################
'''





'''

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

'''