import pull_data
import markov
import random
import facebook

import time
import sys

order = 2
articles = random.randrange(4, 8)

steps = random.randrange(3, 5)
steps_sen = 1

titles_rec_size = 8
steps_rec_size = 5

titles_min_words = 3
steps_min_words = 3


def makeGuide():
    sourceList = pull_data.get_n_articles(articles)
    titleStarts, stepStarts = pull_data.findStartingWordsAndUrls(sourceList, order)
    temp = pull_data.make_plaintext(sourceList)
    tokens = markov.tokenize(temp)
    weights = markov.makeWeights(tokens, order)

    artTitles = []
    for item in sourceList:
        if item[0] == pull_data.textType.TITLE: artTitles.append(item[1])
    text = ''
    #print("title")
    startWords = random.choice(titleStarts)
    numSentences = 1
    minWords = titles_min_words
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, titles_rec_size, titles_min_words))
    text = text[0:len(text)-1]+ ":\n"
    for i in range(steps):
        #print("summary")
        startWords = random.choice(stepStarts)
        numSentences = steps_sen
        minWords = steps_min_words
        text = text + str(i+1) + ": " + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, steps_rec_size, steps_min_words)) + "\n"
    text = text +'\n'

    return text, artTitles

def get_credentials(location='userData.ini'):
    f = open('userData.ini', 'r')
    items = f.read().split()
    f.close()
    page_id = ''
    app_id = ''
    app_secret = ''
    access_token = ''
    page_token = ''
    for i in range(len(items)-1):
        if items[i].lower() == 'page_id=': page_id = items[i+1]
        elif items[i].lower() == 'app_id=': app_id = items[i+1]
        elif items[i].lower() == 'app_secret=': app_secret = items[i + 1]
        elif items[i].lower() == 'access_token=': access_token = items[i + 1]
        elif items[i].lower() == 'page_token=': page_token = items[i + 1]

    return page_id, app_id, app_secret, access_token, page_token

page_id, app_id, app_secret, access_token, page_token = get_credentials()

start = time.time()
text, titles = makeGuide()
#print("access token: "+access_token)
graph = facebook.GraphAPI(access_token= page_token)
print("graph")
#graph.request("0")
post_id = graph.put_object(parent_object=page_id, connection_name='feed', message= text)
print("post_id")
#print(post_id)
print(text)
commentStr = 'ARTICLES USED:'
#for url in urls: commentStr = commentStr + "\n" + url
for title in titles: commentStr = commentStr + "\n" + title[0:len(title)-1]
#commentStr = commentStr + "\n\n" + "(Links temporarily removed to avoid Facebook's spam filter)"
graph.put_comment(object_id=post_id['id'], message=commentStr)
print(commentStr)
#print("time taken: "+ str(time.time()-start)+ "seconds")