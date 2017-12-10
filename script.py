import pull_data
import markov
import random

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

titles_rec_size = 5
abstracts_rec_size = 7
methods_rec_size = 5
summaries_rec_size = 10
steps_rec_size = 5

sourceList = pull_data.get_n_articles(articles)
tStarts, aStarts, mStarts, sStarts, xStarts = pull_data.findStartingWords(sourceList, order)
text = pull_data.make_plaintext(sourceList)
tokens = markov.tokenize(text)
weights = markov.makeWeights(tokens, order)

text = ''
for i in range(titles):
    print("title")
    startWords = random.choice(tStarts)
    numSentences = titles_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, titles_rec_size)) + "\n"
text = text +'\n'
for i in range(abstracts):
    print("abstract")
    startWords = random.choice(aStarts)
    numSentences = abstracts_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, abstracts_rec_size)) + "\n"
#text = text +'\n'
for i in range(methods):
    print("method")
    startWords = random.choice(mStarts)
    numSentences = methods_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, methods_rec_size)) + "\n"
text = text +'\n'
for i in range(summaries):
    print("summary")
    startWords = random.choice(sStarts)
    numSentences = summaries_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, summaries_rec_size)) + "\n"
text = text +'\n'
for i in range(steps):
    print("step")
    startWords = random.choice(xStarts)
    numSentences = steps_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order, steps_rec_size)) + "\n"

print('\n'+text)