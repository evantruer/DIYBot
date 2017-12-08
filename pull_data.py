import json
import urllib.request
import random
import dicttoxml
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser

#initializes random number generator with system time as seed
random.seed()
#max random int value
MAX_VAL = 100000

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
    title = root.find("./app/fulltitle").text
    textList.append(title)
    #abstract = root.find("./app/abstract").text
    abstract = remove_HTML_citations_paren(root.find("./app/sections/item/html").text)
    textList.append(abstract)
    body = root.findall("./app/sections/item/methods/item")
    for section in body:
        #method
        textList.append(remove_HTML_citations_paren(section.find("./name").text))
        steps = section.findall("./steps/item")
        for step in steps:
            #summary
            summary = remove_HTML_citations_paren(step.find("./summary").text)
            textList.append(summary)
            #text
            #print(step.find("./html").text)
            text = remove_HTML_citations_paren(step.find("./html").text)
            textList.append(text)
    return textList


list = make_text_list(rand_wh_page())
for item in list: print(item + "\n")

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