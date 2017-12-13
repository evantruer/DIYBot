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

def makeFacebookPost(text, urls, time):
    return

#print(sys.version)
start = time.time()
text, urls = makeGuide()
print(text)
for url in urls: print("url: "+url)
print("time taken: "+ str(time.time()-start)+ "seconds")