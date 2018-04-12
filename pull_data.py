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
#import markov

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
    # remove whvids
    s = re.sub("\{\{whvid.*\}\}", "", s)
    #
    # remove images
    s = re.sub("\[\[Image:.*\]\]", "", s)
    # replaces wikitext hyperlinks with link text
    s = re.sub("\[\[.*\|", "", s)
    s = re.sub("\]\]", "", s)
    # remove any other [[]]
    s = re.sub("\[\[.*\]\]", "", s)
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
        textList.append((textType.TITLE, title))
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

result = rand_wh_pages(10)
example = parse_page(result)
#print("\n\ncleaned article:")
for line in example:
    print (line[1])
    #if (("{{" in line or "}}" in line) or ("[[" in line or "]]" in line)) or ("<" in line or ">" in line): print("error in: "+line)

#string testing
s = "#* [[Cry and Let It All Out|Cry]][[Image:Become Friends With Your Roommate Step 2.jpg|center]]{{button|Memories}}{{whvid|Build a Wooden Planter Box Step 13.360p.mp4|Build a Wooden Planter Box Step 13-preview.jpg|Build a Wooden Planter Box Step 13.jpg|gif=Build a Wooden Planter Box Step 13.360p.gif|giffirst=Build a Wooden Planter Box Step 13.360p.first.gif}} ''some more''"
#print(clean_wikitext(s))
#print(s)
#s = re.sub("\[\[Image:.*\]\]", "", s)
#print(s)
#s = re.sub("\[\[.*\|", "", s)
#print(s)
#s = re.sub("\]\]", "", s)
#print(s)