from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Achala')

# Create a new trainer for the chatbot
chatbot.set_trainer(ChatterBotCorpusTrainer)

# Train the chatbot based on the english corpus
chatbot.train("corpus")

# Get a response to an input statement

while True:
    qes = input('>')
    rep = chatbot.get_response(qes)
    print(rep)
    if qes == 'quit':
        break