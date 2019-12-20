import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '24f681cca7744966974a6f6149ee028c'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()

request.lang = 'en'  # optional, default value equal 'en'

request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

def getReply(req):
    global request
    
    request.query = req

    response = request.getresponse()
    
    response = response.read().decode('UTF-8')
    print(response)
    
    return response["result"]["fulfillment"]['speech']

def main():
    
    while True:
        req = input('>')
        if(req == "stop"):
            break
        else:
            print(getReply(req))


if __name__ == '__main__':
    main()
