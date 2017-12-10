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

sourceList = pull_data.get_n_articles(articles)
tStarts, aStarts, mStarts, sStarts, xStarts = pull_data.findStartingWords(sourceList, order)
text = pull_data.make_plaintext(sourceList)
tokens = markov.tokenize(text)
weights = markov.makeWeights(tokens, order)

text = ''
for i in range(titles):
    startWords = random.choice(tStarts)
    numSentences = titles_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order)) + "\n"
for i in range(abstracts):
    startWords = random.choice(aStarts)
    numSentences = abstracts_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order)) + "\n"
for i in range(methods):
    startWords = random.choice(mStarts)
    numSentences = methods_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order)) + "\n"
for i in range(summaries):
    startWords = random.choice(sStarts)
    numSentences = summaries_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order)) + "\n"
for i in range(steps):
    startWords = random.choice(xStarts)
    numSentences = steps_sen
    text = text + markov.formatOutput(markov.makeText(weights, startWords, numSentences, True, order)) + "\n"

print(text)