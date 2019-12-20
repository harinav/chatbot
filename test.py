from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

import warnings
warnings.filterwarnings("ignore")

class OfficeAgent():
    def __init__(self):
        messages = ["Hi! you can chat in this window. Type 'stop' to end the conversation."]
        interpreter = RasaNLUInterpreter("./models/nlu/default/nlu_model")
        self.inter = interpreter
        action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
        self.agent = Agent.load("./models/dialogue/default/dialogue_model", interpreter=interpreter,action_endpoint = action_endpoint)
        print(messages[0])
    
    def exec_query(self, query, sender_id): 
	    responses = self.agent.handle_message(message=query,sender_id=sender_id)
	    print(responses)
	    if 'action' in responses[0]['text']:
		    return responses[0]
	    result = {'recipient_id': responses[0]['recipient_id'], 'text': str({'action':'bot_action','teams_msg':'', 'email':'', 'yout_url':'', 'sloc':'', 'eloc':'', 'result':responses[0]['text']})}
	    print(result)
	    return result
