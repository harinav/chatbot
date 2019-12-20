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
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def agent(user_message):
    request = ai.text_request()
    request.query = user_message

    response = json.loads(request.getresponse().read())

    result = response['result']
    action = result.get('action')
    actionIncomplete = result.get('actionIncomplete', False)

    #print(u"< %s" % response['result']['fulfillment']['speech'])
    return response['result']['fulfillment']['speech']