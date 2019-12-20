from __future__ import print_function

import os
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )

    import apiai


# demo agent acess token: e5dc21cab6df451c866bf5efacb40178

CLIENT_ACCESS_TOKEN = '0878b3d05b33446fbf5a4b6263bc836f'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    user_message = raw_input('>')
    
    request.query = user_message
    
    sess_id = request._session_id
    name = ''
    id = ''
    
    while True:
        sess_id_temp = sess_id + ","+name+","+id
        request.session_id = sess_id_temp
        response = json.loads(request.getresponse().read())
        
        print('response',response)
        
        
        result = response['result']
        action = result.get('action')
        
        print("< %s" % response['result']['fulfillment']['speech'])

        if action is not None:
            if(action == "authentication"):
                name = result.get('parameters').get('given-name')
                id = result.get('parameters').get('email')
            elif(action == "stop"):
                name = ''
                id = ''
                ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        user_message = raw_input('>')

        if user_message == "exit":
            break
        
        request = ai.text_request()
        
        try:
            if(str(response['result']['parameters']['bank-name']) == "HDFC Bank"):
                request.session_id = response['result']['parameters']['bank-name']
                print(request._session_id)
        except:
            print()
        
        request.query = user_message


if __name__ == '__main__':
    main()