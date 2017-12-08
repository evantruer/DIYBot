import bisect


#Splits a string s into tokens and return a list of strings
#Right now, just calls str.split() but may later be updated to split punctuation
def tokenize(s):
    return s.split()

#Generates Markov chain weights for list tokens and order ord
#Returns a list of two element tuples:
# Element 0 is the current state (list of tokens of length <= ord)
# Element 1 is a list of two element tuples:
#  Element A is a possible next token
#  Element B is the number of times A has appeared
def makeWeights(tokens, ord=1):
    #takes the list, current state, and token, and updates the list
    def updateWeights(l, state, token):
        j = 0
        foundState = False
        stateIndex = -1
        while j < len(l):
            if l[j][0] == state :
                foundState = True
                stateIndex = j
                break
            j = j + 1
        if foundState :
            state = l[j]
            tokenWeights = state[1]

            k = 0
            foundWeight = False
            weightIndex = -1
            while k < len(tokenWeights) :
                if tokenWeights[k][0] == token :
                    foundWeight = True
                    weightIndex = k
                    break
                k = k + 1
            if foundWeight :
                placeholder = 0
            else :
                #CONTINUE HERE
        else :
            l.append((state, [(token, 1)]))
        return l

    weights = []
    currentState = []
    i = 0
    while i < len(tokens)-1:
        currentState.append(tokens[i])
        if len(currentState) > ord :
            currentState.pop(0)
         weights = updateWeights(weights, currentState, tokens[i+1])
        i = i + 1
