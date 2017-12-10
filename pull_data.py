import json
import urllib.request
import random
import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser
from enum import Enum
import markov

#initializes random number generator with system time as seed
random.seed()
#max random int value
MAX_VAL = 100000

class textType(Enum):
    TITLE = 1
    ABSTRACT = 2
    METHOD = 3
    SUMMARY = 4
    TEXT = 5

#Pulls the webpage specified by url.
def get_page(url):
    page = urllib.request.urlopen(url)
    return page.read()

#Pulls a random WikiHow article in JSON format.
#The WikiHow API allows for the pulling of random articles.
#However, if the same URL is used twice, it will return the same article.
#To solve this, the  API "_" subcommand is used with a random argument in order to get around this.
#Its argument is ignored but this changes the URL.
def rand_wh_page():
    randInt = str(random.randrange(MAX_VAL))
    #print("random val: "+randInt)
    page = get_page("https://wikihow.com/api.php?action=app&subcmd=article&format=json&random=true&_=" + randInt)
    #page = get_page("https://wikihow.com/api.php?action=app&subcmd=article&format=json&name=Ripen-Bananas-Quickly")
    return page

#converts page from JSON to XML format
def convert_to_xml(page):
    obj = json.loads(page)
    xml = dicttoxml.dicttoxml(obj)
    #print(str(xml))
    return xml



#Takes page and returns a list of words that the page's section titles start with.
#count is the number of words to pull from the start of each section title.
#If count is greater than the number of words in the section title the entire title is returned.
def get_first_sec_words(page, count = 1):
    jsonPage = json.loads(page)
    firstWords =  []
    return

#removes HTML tags and citations from a string s
def remove_HTML_citations_paren(s):
    if str(s) == "None" : return ""
    #remove HTML tags
    s = re.sub("<[^>]+>", "", s)
    #remove citations
    s = re.sub("\[[\d]+\]", "", s)
    #remove parentheses
    s = re.sub("\([^)]+\)", "", s)
    #remove quotation marks
    s = re.sub("\"", "", s)
    return s

#Returns a list of all titles, abstracts, method titles, step summaries, and step texts
#in page in order of appearance.
#In other words, it makes the article into a list
def make_text_list(page):
    #get a page in XML format
    xmlPage = convert_to_xml(page)
    root = ET.fromstring(xmlPage)
    #getting url
    url = root.find("./app/url").text
    print(url)
    print("\n")
    textList = []
    title = root.find("./app/fulltitle")
    if title is not None: textList.append((textType.TITLE, title.text + "."))
    abstract = root.find("./app/sections/item/html")
    if abstract is not None: textList.append((textType.ABSTRACT, remove_HTML_citations_paren(abstract.text)))
    #abstract = remove_HTML_citations_paren(root.find("./app/sections/item/html").text)
    #textList.append((textType.ABSTRACT, abstract))
    body = root.findall("./app/sections/item/methods/item")
    for section in body:
        #method
        method = section.find("./name")
        if method is not None: textList.append((textType.METHOD, remove_HTML_citations_paren(method.text)))
        steps = section.findall("./steps/item")
        for step in steps:
            #summary
            summary = step.find("./summary")
            if summary is not None: textList.append((textType.SUMMARY, remove_HTML_citations_paren(summary.text)))
            #text
            text = step.find("./html")
            if text is not None: textList.append((textType.TEXT, remove_HTML_citations_paren(text.text)))
    return textList

def findStartingWords(textList, ord = 1):
    titleStarts = []
    abstractStarts = []
    methodStarts = []
    summaryStarts = []
    textStarts = []
    for item in textList :
        splitText = markov.tokenize(item[1])
        newStartWords = []
        #skip over very short starting phrases
        if len(splitText) < ord : continue
        for i in range(ord):
            newStartWords.append(splitText[i])
            newTuple = tuple(newStartWords)
        if item[0] == textType.TITLE:
            titleStarts.append(newTuple)
        elif item[0] == textType.ABSTRACT :
            abstractStarts.append(newTuple)
        elif item[0] == textType.METHOD :
            methodStarts.append(newTuple)
        elif item[0] == textType.SUMMARY :
            summaryStarts.append(newTuple)
        else :
            textStarts.append(newTuple)
    return titleStarts, abstractStarts, methodStarts, summaryStarts, textStarts

#makes a plaintext out of a text list
def make_plaintext(textList):
    s = ""
    for item in textList : s = s + item[1] +'\n'
    return s

#gets a combined text list of all n articles
def get_n_articles(n=5):
    out = []
    for i in range(n):
        out = out + make_text_list(rand_wh_page())
    return out

#list = make_text_list(rand_wh_page())
#for item in list: print(item[1] + "\n")

#TESTING_CODE
#print(str(get_page("https://wikihow.com/api.php?action=app&subcmd=article&format=json&random=true&_=")))
#print(str(rand_wh_page()))
#get_first_sec_words(rand_wh_page())

#if(False):
#    xml_page = convert_to_xml(rand_wh_page())
#    dom = parseString(xml_page)
#    pretty = dom.toprettyxml()
#    f = open("xml_test.txt", "w", encoding="utf-8")
#    f.write(pretty)
#    f.close()