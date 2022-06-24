# import requirements needed
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, make_response
from utils import get_base_url
from aitextgen import aitextgen
import re
from random import randint
# Get rid of warning
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12348
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')


app.secret_key = os.urandom(64)


# Loading Models
#WORK NO TOUCH
ai_ironman = aitextgen(model_folder="model/trained_model-ironman",
                tokenizer_file="model/aitextgen.tokenizer-ironman.json", TF_ENABLE_ONEDNN_OPTS=0)
#NEEDS TESTING
ai_thor = aitextgen(model_folder="model/trained_model-thor",
                tokenizer_file="model/aitextgen.tokenizer-thor.json", TF_ENABLE_ONEDNN_OPTS=0)
#NEEDS TESTING
ai_spiderman = aitextgen(model_folder="model/trained_model-spiderman",
                tokenizer_file="model/aitextgen.tokenizer-spiderman.json", TF_ENABLE_ONEDNN_OPTS=0)

#WORKING NO TOUCH
def filter(user_input, ai_gen):
    length = len(user_input) - 1
    if user_input[length] == '?':
        user_input = user_input[0:length] + '.'
    if user_input[length] != '.' and user_input[length] != '!':
         user_input = user_input + '.'
    chat_bot_output = ai_gen

    # Regular expression
    text = re.sub(r'\n',' ',chat_bot_output)
    text = re.sub(r'%s' % user_input, '', text)

    # also, take out the cuttoff sentence at the end
    tempText = text[::-1]
    cutOffPeriod = tempText.find(".")
    cutOffEx = tempText.find("!")
    cutOffQuestion = tempText.find("?")

    #need to find lowest index thats not below zero
    listOfCut = [cutOffPeriod,cutOffEx,cutOffQuestion]
    listOfCut.sort()
    cutOff = -2;#needs to be less than -1
    index = 0;
    while(cutOff<=-1 and index < 3):
        cutOff = listOfCut[index]
        index = index + 1
    #ensures that if text doesn't have puncuation the program won't crash
    if(cutOff==-2):
        text = text + "."
        cutOff = len(text) - 1
    # match = re.sub(r"%s" % user_input, '')
    return text[length:len(text)-cutOff + 1].strip()

#WORKING NO TOUCH
# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')

### ironman page
@app.route(base_url + '/ironman')
def ironman():
    return render_template('ironman.html')

### ironman generation page
@app.route(base_url + '/genironman/<lastUserMessage>')
def genironman(lastUserMessage):
    print("HELLO")
    print(lastUserMessage)
    ai_gen = ai_ironman.generate_one(batch_size=32, prompt=lastUserMessage, max_length=40, temperature=.8, top_p=0.9)
    ai_gen = re.sub(r'\n',' ',ai_gen)
    ai_gen = re.sub(r'%s' % lastUserMessage, '', ai_gen)
    return jsonify(ai_gen)

### spiderman page
@app.route(base_url + '/spiderman')
def spiderman():
    return render_template('spiderman.html')

### spiderman generation page
@app.route(base_url + '/genspiderman/<lastUserMessage>')
def genspiderman(lastUserMessage):
    print("HELLO")
    print(lastUserMessage)
    ai_gen = ai_spiderman.generate_one(batch_size=32, prompt=lastUserMessage, max_length=40, temperature=.8, top_p=0.9)
    ai_gen = re.sub(r'\n',' ',ai_gen)
    ai_gen = re.sub(r'%s' % lastUserMessage, '', ai_gen)
    return jsonify(ai_gen)

### thor page
@app.route(base_url + '/thor')
def thor():
    return render_template('thor.html')

### spiderman generation page
@app.route(base_url + '/genthor/<lastUserMessage>')
def genthor(lastUserMessage):
    print("HELLO")
    print(lastUserMessage)
    ai_gen = ai_thor.generate_one(batch_size=32, prompt=lastUserMessage, max_length=40, temperature=.8, top_p=0.9)
    ai_gen = re.sub(r'\n',' ',ai_gen)
    ai_gen = re.sub(r'%s' % lastUserMessage, '', ai_gen)
    return jsonify(ai_gen)

### groot page
@app.route(base_url + '/groot')
def groot():
    return render_template('groot.html')

### groot generation page
@app.route(base_url + '/gengroot/<lastUserMessage>')
def gengroot(lastUserMessage):
    print("HELLO")
    print(lastUserMessage)
    number2 = randint(1 ,1000)
    number = randint(1, 1000)
    if (number2 in range(1, 100)):
        ai_gen = "I am Groooooooooooooot!"
    elif (number2 in range(101, 200)):
        ai_gen = "I am Groot?"
    elif (number2 in range(201, 300)):
        ai_gen = "I! AM! GROOT!"
    else:
        ai_gen = "I am Groot."
    if number == number2:
        ai_gen = "We are Groot"
    return jsonify(ai_gen)


#NO TOUCH IT WORKS
@app.route(base_url + '/product')
def product():
    return render_template('productSpec.html')

@app.route(base_url + '/about')
def about():
    return render_template('aboutUsPage2.html')


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalcg8.ai-camp.dev/'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
