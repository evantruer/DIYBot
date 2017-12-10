import string
from pathlib import Path
import random
import pull_data


#Splits a string s into tokens and return a list of strings
#Right now, just calls str.split() on a lowercased text and then separates punctuation
def tokenize(s):
    tokenList = s.lower().split()
    newList = []
    for token in tokenList:
        if token[len(token)-1].isalnum() == False:
            newList.append(token[:len(token) - 1])
            newList.append(token[len(token) - 1])
        else :
            newList.append(token)
    return newList

#Generates Markov chain weights for list tokens and order ord
#Returns a dictionary:
# Keys are tuples of strings and represent the current state
# Values are themselves dictionaries:
#  Keys are strings (each possible next token)
#  Values are positive integers (how many times a specific token appears after the current state)
def makeWeights(tokens, ord=1):
    #The dictionary we'll be working on.
    weights = {}
    #Return an empty dictionary if tokens has less than 2 items.
    #If this is true, there is no token with another token after it.
    if len(tokens) <= 1 : return weights
    #The main loop; goes through each token except the first.
    #We maintain a list of the last ord tokens.
    #The first token is added to this list automatically.
    currentState = []
    currentState.append(tokens[0])
    for nextToken in tokens[1:]:
        #print(str(currentState))
        #We have to convert currentState to a tuple to use as a dictionary key.
        dictKey = tuple(currentState)
        if dictKey in weights :
            #This means we need to modify an existing key.
            if nextToken in weights[dictKey] :
                #This means [...currentState, nextToken,...] has appeared before in tokens.
                #So we increment an already existing weight.
                weights[dictKey][nextToken] = weights[dictKey][nextToken] + 1
            else :
                #Otherwise, we must add nextToken to dictionary weights[dictKey] with value 1.
                weights[dictKey][nextToken] = 1

        else :
            #dictKey not in weights -> first occurrence of dictKey.
            #Therefore, we know that we can add it as a key
            #with its value indicating that the only possible next token
            #is nextToken, with weight 1.
            weights[dictKey] = {nextToken : 1}
        #Now we modify currentState in preparation for the next iteration.
        currentState.append(nextToken)
        if len(currentState) > ord : currentState.pop(0)
    return weights

#TODO: Description
def makeText(weights, startWords=None, numSentences=1, respectWeights=True, ord=1, endSenAt=5):
    #We choose a random starting state if startWords defaults to None.
    currentState = list(startWords)
    if currentState is None :  currentState = random.choice(list(weights.keys()))
    #Man loop. Generates text until numSentences sentences are reached.
    #Specficially, numSentences is decremented every time we find '.', '?', or '!'
    textList = []
    for token in currentState: textList.append(token.lower())
    numWords = ord
    while numSentences > 0:
        currentWeights = weights[tuple(currentState)]
        nextToken = ''
        try:
            if numWords >= endSenAt and '.' in currentWeights :
                nextToken = '.'
                print("punctuation auto-selected\n")
            elif numWords >= endSenAt and '!' in currentWeights:
                nextToken = '!'
                print("punctuation auto-selected\n")
            elif numWords >= endSenAt and '?' in currentWeights:
                nextToken = '?'
                print("punctuation auto-selected\n")
            elif respectWeights:
                #TODO choose randomly according to weights
                nextToken = random.choice(list(currentWeights.keys()))
            else:
                #Choose as if all weights are 1
                nextToken = random.choice(list(currentWeights.keys()))
        #This is to handle an edge case:
        #Basically, if the current state represents the last ord tokens in the text,
        #and said token sequence appears nowhere else, there's no "next token."
        #The only logicl solution is to terminate early even if there are still more sentences to generate.
        except KeyError: return textList
        numWords = numWords+1
        textList.append(nextToken)
        currentState.append(nextToken)
        if len(currentState) > ord : currentState.pop(0)
        #tempBool exists for readability
        tempBool = currentState[len(currentState)-1] == '.'
        tempBool = tempBool or currentState[len(currentState) - 1] == '?'
        tempBool = tempBool or currentState[len(currentState) - 1] == '!'
        if tempBool :
            numSentences = numSentences - 1
            numWords = 0
    return textList

def formatOutput(outList):
    out = string.capwords(outList[0])
    for word in outList[1:]:
        space = " "
        if len(word) == 0 or word[len(word) - 1].isalnum() == False: space = ''
        if out[len(out) - 1] == '.' or out[len(out) - 1] == '?' or out[len(out) - 1] == '!':
            word = string.capwords(word)
            space = ' '
        out = out + space + word
    return out


#order = 2
#s = Path("multiTest.txt").read_text()
#weights = makeWeights(tokenize(s),order)
#for key in weights : print(str(key) +": " + str(weights[key]))
#text = makeText(weights, ['how'], 5, False, order)
#out = string.capwords(text[0])
#for word in text[1:]:
    #space = " "
    #if len(word) == 0 or word[len(word)-1].isalnum() == False: space = ''
    #if out[len(out)-1] == '.' or out[len(out)-1] == '?' or out[len(out)-1] == '!':
        #word = string.capwords(word)
        #space = ' \n'
    #out = out + space + word
#print(out)