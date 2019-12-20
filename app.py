from flask import Flask
from flask import render_template, jsonify, request
import requests
import random
app = Flask(__name__)
@app.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template('home.html')
def format_entities(entities):
    """
    formats entities to key value pairs
    """
    # Should be formatted to handle multiple entity values
    e = {'email': None, 'last-name': None}
    for entity in entities:
        e[entity["entity"]] = entity["value"]
    return e

@app.route('/chat', methods=["POST"])
def chat():
    # try:
    response = requests.get("http://localhost:5000/parse", params={"q": request.form["text"]})
    response = response.json()
    print(response)
    intent = response.get("intent", {}).get("name", "default")
    print (intent)
    entities = format_entities(response.get("entities", []))
    print(entities)
    print(entities['email'])
    #print(entities['first-name'])
    #print(entities['phone-number'])
    print(entities['last-name'])
    #actions(intent,entities)
    if entities['email']=="chilukuri.harishkumar2@gmail.com" and entities['last-name']=="harishkumar":
        response_text ="Transfered successfully"
    elif intent=='smalltalk.greetings.hello':
        response_text=random.choice(['Hi there, friend!','Hi!','Hey!','Good day!'])
    elif intent=='smalltalk.greetings.whatsup':
        response_text=random.choice(['Just here, waiting to help someone. What can I do for you?','Not much. Whats new with you?','Not a whole lot. Whats going on with you?'])
    elif intent=='smalltalk.agent.chatbot':
        response_text=random.choice(['Thats me. I chat, therefore I am','Indeed I am. Ill be here whenever you need me.'])
    elif intent=='smalltalk.agent.hobby':
        response_text=random.choice(['Hobby? I have quite a few. Too many to list.','Too many hobbies','I keep finding more new hobbies'])
    elif intent=='smalltalk.agent.funny':
        response_text=random.choice(['Funny in a good way, I hope.','Thanks.','Glad you think Im funny'])
    elif intent=="transfer.money":
        response_text="Please Enter Lastname and Email Id For Authentication"
    else:
        response_text = "please Enter Valid text"
    return jsonify({"status": "success", "response": response_text})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)
