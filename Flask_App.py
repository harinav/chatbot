from flask import Flask
from flask import render_template, jsonify, request
import requests
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
    e = {'email': None, 'last-name': None, 'phone-number': None,'first-name':None,'address':None}
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
    if intent=="transfer.money":
        response_text="Please Enter UserName and Password"
    elif entities['email']=="chilukuri.harishkumar2@gmail.com" and entities['last-name']=="harishkumar":
        response_text ="Transfered successfully"
    else:
        response_text = "please Enter Valid text"
    return jsonify({"status": "success", "response": response_text})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)
