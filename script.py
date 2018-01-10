import pull_data
import markov
import random
import facebook

import time
import sys

order = 2
articles = 5


titles = 1
abstracts = 0
methods = 0
summaries = 3
steps = 0

titles_sen = 1
abstracts_sen = 3
methods_sen = 1
summaries_sen = 1
steps_sen = 2

titles_rec_size = 8
abstracts_rec_size = 7
methods_rec_size = 8
summaries_rec_size = 13
steps_rec_size = 5

titles_min_words = 3
abstracts_min_words = 7
methods_min_words = 5
summaries_min_words = 13
steps_min_words = 5


def makeGuide():
    sourceList = pull_data.get_n_articles(articles)
    tStarts, aStarts, mStarts, sStarts, xStarts, urls = pull_data.findStartingWordsAndUrls(sourceList, order)
    text = pull_data.make_plaintext(sourceList)
    tokens = markov.tokenize(text)
    weights = markov.makeWeights(tokens, order)

    text = ''
    for i in range(titles):
        #print("title")
        startWords = random.choice(tStarts)
        numSentences = titles_sen
        minWords = titles_min_words
        text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, titles_rec_size, titles_min_words)) + "\n"
    #text = text +'\n'
    for i in range(abstracts):
        #print("abstract")
        startWords = random.choice(aStarts)
        numSentences = abstracts_sen
        minWords = abstracts_min_words
        text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, abstracts_rec_size, abstracts_min_words)) + "\n"
    #text = text +'\n'
    for i in range(methods):
        #print("method")
        startWords = random.choice(mStarts)
        numSentences = methods_sen
        minWords = methods_min_words
        text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, methods_rec_size, methods_min_words)) + "\n"
    text = text +'\n'
    for i in range(summaries):
        #print("summary")
        startWords = random.choice(sStarts)
        numSentences = summaries_sen
        minWords = summaries_min_words
        text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, summaries_rec_size, summaries_min_words)) + "\n"
    text = text +'\n'
    for i in range(steps):
        #print("step")
        startWords = random.choice(xStarts)
        numSentences = steps_sen
        minWords = steps_min_words
        text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, steps_rec_size, steps_min_words)) + "\n"

    return text, urls

def get_credentials(location='userData.ini'):
    f = open('userData.ini', 'r')
    items = f.read().split()
    f.close()
    page_id = ''
    app_id = ''
    app_secret = ''
    access_token = ''
    for i in range(len(items)-1):
        if items[i].lower() == 'page_id=': page_id = items[i+1]
        elif items[i].lower() == 'app_id=': app_id = items[i+1]
        elif items[i].lower() == 'app_secret=': app_secret = items[i + 1]
        elif items[i].lower() == 'access_token=': access_token = items[i + 1]

    return page_id, app_id, app_secret, access_token

page_id, app_id, app_secret, access_token = get_credentials()

start = time.time()
text, urls = makeGuide()
#print("access token: "+access_token)
graph = facebook.GraphAPI(access_token= access_token)
graph.put_object(parent_object=page_id, connection_name='feed', message= text)

print(text)
for url in urls: print("url: "+url)
print("time taken: "+ str(time.time()-start)+ "seconds")