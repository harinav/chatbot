import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import markovify #Markov Chain Generator
import random

inp = pd.read_csv('test_data.csv')

text_model = markovify.NewlineText(inp.questions, state_size = 2)

print(text_model.chain.to_json())
for i in range(10):
    print(text_model.make_sentence())
    