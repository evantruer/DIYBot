import json
import urllib.request
import random
import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser
from enum import Enum
import xml
import string
import markov

class textType(Enum):
    END = 0
    TITLE = 1
    TEXT = 2

#Pulls the webpage specified by url.
def get_page(url):
    page = urllib.request.urlopen(url)
    return page.read().decode("utf-8")

#Pulls n random WikiHow articles in XML format
def rand_wh_pages(n):
    pages = get_page("https://www.wikihow.com/api.php?action=query&generator=random&grnnamespace=0&grnlimit="+str(n)+"&export&exportnowrap")
    return pages

#cleans Wikitext from a string
#After the old method of pulling data broke, I had to resort to pulling
#from the API in a different format which preserved WikiText.
#This is a major issue because there's no easy way to clean the text anymore.
#I couldn't find documentation so there might be some things that aren't filtered
#even though I've skimmed through dozens of exported WikiHow articles to find
#the different forms WikiText generally takes on WikiHow.
#
#WikiHow itself isn't very forthcoming with API stuff.
#The author of another bot asked WikiHow about said breaking API update.
#Instead of fixing the issue, they sent him an angry message telling him to
#shut down his bot. Since his bot was publishing their content and mine isn't,
#there's no worry as far as legality is concerned but I'm not going to ask
#WikiHow to fix their API.
def clean_wikitext(s):
    if str(s) == "None" : return ""
    # remove hyperlinks
    s = re.sub("<ref>.*</ref>", "", s)
    # remove HTML tags
    s = re.sub("<[^>]+>", "", s)
    # remove #*
    s = re.sub("#\*", "", s)
    # remove #
    s = re.sub("#", "", s)
    #Cleaning/removal of things in double brackets
    #We start by noting where [[, ]], {{, and }} are
    curly_starts = []
    curly_ends = []
    square_starts = []
    square_ends = []
    #Note that for every start double bracket there is a corresponding and double bracket
    #which occurs before any other double bracket
    i = 1
    while i < len(s):
        if s[i - 1] == "{" and s[i] == "{": curly_starts.append(i - 1)
        if s[i - 1] == "}" and s[i] == "}": curly_ends.append(i)
        if s[i - 1] == "[" and s[i] == "[": square_starts.append(i - 1)
        if s[i - 1] == "]" and s[i] == "]": square_ends.append(i)
        i = i+1
    #Now we decide what we need to replace the double brackets with
    replacements = []
    # Since what we want to do is dependent on the type of brace, we handle them separately
    while len(curly_starts) > 0 and len(curly_ends) > 0:
        #Get the bounds of a pair of double braces
        start = curly_starts.pop()
        end = curly_ends.pop()
        toReplace = s[start:end+1]
        #Double brackets usually have "token1|token2|..." inside of them
        tokens = str.split(toReplace[2:len(toReplace)-2], "|")
        #There are a some things we just want to delete
        #They generally mean things like "add a video/image"
        #We know that if the first token starts with certain things, we want to move on
        def should_ignore(token_list):
            ignore_list = ["whvid", "video", "Video", "pictures", "Pictures", "stub", "Stub", "reflist", "fa", "intro", "Intro"]
            for item in ignore_list:
                if token_list[0].startswith(item):
                    return True
            return False
        #If we should ignore, then we replace the brackets with nothing
        if should_ignore(tokens):
            replacements.append((toReplace, ""))
        #otherwise, we need to look at it closer
        else:
            #If the first token is "convert", we need to replace it with "<number>" "<unit>":
            if tokens[0] == "convert":
                #a list of all units
                length_abbr = "mm cm m km in ft mi "
                length = "millimeter centimeter meter kilometer inch foot mile "
                area_abbr = "cm2 m2 sqft ft2 sqmi mi2 "
                area = "acre hectare "
                mass_abbr = "g kg USoz lb "
                mass = "gram kilogram ounce pound "
                volume_abbr = "ml L USgal UStbsp USts "
                volume = "millileter liter gallon tablespoon teaspoon "
                speed_abbr = "mph kph "
                speed = "milesperhour kilometersperhour "
                time_abbr = "s min hr yr "
                time = "second minute hour day month year "
                units = str.split(length_abbr+length+area_abbr+area+mass_abbr+mass+volume_abbr+volume+speed_abbr+speed+time_abbr+time)
                #defaults to 5 cm
                chosenUnit = "cm"
                chosenValue = "5"
                for token in tokens:
                    if token in units:
                        chosenUnit = token
                        break
                for token in tokens:
                    if any(char.isdigit() for char in token):
                        chosenValue = token
                        break
                replacements.append((toReplace, chosenValue + " "+chosenUnit))
            #if the first token is "keypress" we want to render as all tokens but the first separated by dashes
            elif tokens[0] == "keypress" and len(tokens) > 1:
                press = tokens[1]
                for token in tokens[2:]:
                    press = press + "-" + token
                replacements.append((toReplace, press))
            #If there are 2 tokens and it's not in any of the other cases it's usually some specially formatted text
            #In this case, the second token is what a WikiHow user would see
            elif len(tokens) == 2:
                replacements.append((toReplace, tokens[1]))
    while len(square_starts) > 0 and len(square_ends) > 0:
        # Get the bounds of a pair of double braces
        start = square_starts.pop()
        end = square_ends.pop()
        toReplace = s[start:end + 1]
        # Double brackets usually have "token1|token2|..." inside of them
        tokens = str.split(toReplace[2:len(toReplace) - 2], "|")

        # There are a some things we just want to delete
        # They generally mean things like "add a video/image"
        # We know that if the first token starts with certain things, we want to move on
        def should_ignore(token_list):
            ignore_list = ["Category", "Image"]
            for item in ignore_list:
                if token_list[0].startswith(item):
                    return True
            return False

        # If we should ignore, then we replace the brackets with nothing
        if should_ignore(tokens):
            replacements.append((toReplace, ""))
        # otherwise, we need to look at it closer
        else:
            # If there are 2 tokens and it's not in any of the other cases it's usually some specially formatted text
            # In this case, the second token is what a WikiHow user would see
            if len(tokens) == 2:
                replacements.append((toReplace, tokens[1]))
            #if there's one token, we assume it should be printed
            elif len(tokens) == 1:
                replacements.append((toReplace, tokens[0]))
    #We let regular expressions handle the rest
    for replacement in replacements:
        #print("replacing "+replacement[0]+ " with "+replacement[1])
        #we have to escape replacement[0]
        s = re.sub(re.escape(replacement[0]), replacement[1], s)
    #remove multiple single quotation marks
    s = re.sub("'{2,100}", "", s)
    punctuation = [".", "?", "!"]
    if  len(s) > 0 and s[len(s)-1] not in punctuation:
        s += '.'
    return s.lstrip()

#Takes the query result in XML format and parses it into a list of titles and steps in order
def parse_page(queryResult):
    namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
    #print(queryResult)
    #root = ET.ElementTree(ET.fromstring(queryResult))
    root = ET.fromstring(queryResult)
    #print(ET.tostring(root, method="xml", encoding="unicode"))
    textList = []
    articles = root.findall(namespace+"page")
    print("number of articles: " + str(len(articles)))
    for article in articles:
        #print("article found")
        #print(ET.tostring(article, method="xml", encoding="unicode"))
        title = "How To "+ article.find(namespace+"title").text
        textList.append((textType.TITLE, title + "."))
        temp = article.find(namespace+"revision")
        text = temp.find(namespace+"text").text
        #print("article text:\n"+text)
        linesList = text.splitlines()
        class states(Enum):
            ABSTRACT = 0
            CATEGORIES = 1
            STEPS = 2
        state = states.ABSTRACT
        abstract = ""
        for line in linesList:
            #print(state)
            #print(line)
            if state == states.ABSTRACT:
                abstract = clean_wikitext(line)
                state = states.CATEGORIES
            elif state == states.CATEGORIES:
                if re.match("\=\= *Steps *\=\=", line):
                    state = states.STEPS
            elif state == states.STEPS:
                if line.startswith("==") and line.startswith("===") == False:
                    textList.append((textType.END, "END_OF_ARTICLE"))
                    break
                if line.startswith('==='):
                    continue
                else:
                    if len(line) > 0: textList.append((textType.TEXT, clean_wikitext(line)))

    return textList



#Returns the first ord words of every part of the article, put into lists
#based on what type of line it is
def findStartingWordsAndUrls(textList, ord = 1):
    titleStarts = []
    textStarts = []
    for item in textList :
        #print(item[1])
        splitText = markov.tokenize(item[1])
        newStartWords = []
        #skip over very short starting phrases
        if len(splitText) < ord : continue
        for i in range(ord):
            newStartWords.append(splitText[i])
            newTuple = tuple(newStartWords)
        if item[0] == textType.TITLE:
            titleStarts.append(newTuple)
        elif item[0] == textType.TEXT:
            textStarts.append(newTuple)
    return titleStarts, textStarts

#makes a plaintext out of a text list
def make_plaintext(textList):
    s = ""
    for item in textList:
        if item[0] != textType.END: s = s + item[1] +'\n'
    return s

#gets a combined text list of n articles
def get_n_articles(n):
    pages = rand_wh_pages(n)
    lineList = parse_page(pages)
    out = []
    for line in lineList:
        if line[0] is not textType.END:
            out.append(line)
    return out



#result = rand_wh_pages(10)
#example = parse_page(result)
#print("\n\ncleaned article:")
#for line in example:
#    #break
#    print (line[1])
#print(get_n_articles(10))