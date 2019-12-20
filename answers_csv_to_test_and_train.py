import pandas as pd
import time

def format_data(data):
    data = data.replace('\n',' ').replace('\r',' ').replace('"',"'").replace('<p>','').replace('</p>','').\
           replace('<pre>','').replace('</pre>','').replace('<code>', '').replace('</code>','').replace('<br>','').\
           replace('<hr>','').replace('<ul>','').replace('</ul>','').replace('<li>','').replace('</li>','').\
           replace('</a>','').replace('<a>','').replace('<a ','').replace('\t','').replace('   ','').replace('<blockquote>','')\
           .replace('</blockquote>','').replace('<strong>','').replace('</strong>','').replace('<em>','').replace('</em>','')\
           .replace('<br />','').replace('<ol>','').replace('</ol>','').replace('<pre ','').replace('<i>','').replace('</i>','')\
           .replace('<h3>','').replace('</h3>','').replace('<H2>','').replace('</H2>','').replace('<h2>','').replace('</h2>','')\
           .replace('<h1>','').replace('</h1>','').replace('</A>','').replace('<A>','')
    return data


answers = dict()

st = time.time()
data = pd.read_csv("Answers.csv", sep=',',encoding="ISO-8859-1")
et = time.time()
print(et-st)

for i in range(987122):
    #print(data['ParentId'][i],'\t',data['Score'][i])
    if(i%1000 == 0):
        print('Processed {} lines.'.format(i))
    key = data['ParentId'][i]
    score = data['Score'][i]
    body = format_data(data['Body'][i])
    if key in answers:
        # append the new number to the existing array at this slot
        if answers[key][0] < score:
            answers[key][0] = score
            answers[key][1] = body
    else:
        # create a new array in this slot
        answers[key] = [score]
        answers[key].append(body)

count = 0
with open('test.to','a', encoding='utf8') as f:
    for key in sorted(answers):
        count += 1
        if(count <= 100000):
            f.write(str(answers[key][1])+'\n')
        if(count%1000 == 0):
            print('{} lines store to test1.to file.'.format(count))
count = 0
with open('train.to','a', encoding='utf8') as f:
    for key in sorted(answers):
        count += 1
        if(count > 100000):
            f.write(str(answers[key][1])+'\n')
        if(count%1000 == 0):
            print('{} lines store to train1.to file.'.format(count))
print(len(answers.keys()))    