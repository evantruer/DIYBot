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
    return get_page("https://wikihow.com/api.php?action=app&subcmd=article&format=json&random=true&_=" + randInt)

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
def remove_HTML_and_citations(s):
    #replace HTML tags with spaces
    s = re.sub("<[^>]+>", "", s)
    #remove citations
    s = re.sub("\[[\d]+\]", "", s)
    return s

#TESTING_CODE
#print(str(get_page("https://wikihow.com/api.php?action=app&subcmd=article&format=json&random=true&_=")))
#print(str(rand_wh_page()))
#get_first_sec_words(rand_wh_page())

if(False):
    xml_page = convert_to_xml(rand_wh_page())
    dom = parseString(xml_page)
    pretty = dom.toprettyxml()
    f = open("xml_test.txt", "w", encoding="utf-8")
    f.write(pretty)
    f.close()

for i in range(1):
    #get a page in XML format
    xml_page = convert_to_xml(rand_wh_page())
    root = ET.fromstring(xml_page)
    #query title
    title = root.find("./app/fulltitle").text
    print("title: "+title)

    url = root.find("./app/url").text
    print("url: " + url)

    abstract = root.find("./app/abstract").text
    print("abstract:")
    print(remove_HTML_and_citations(abstract))

    methods = root.findall("./app/sections/item/methods/item/name")
    print("\nmethods: ")
    for method in methods:
        print(method.text)


    summaries = root.findall("./app/sections/item/methods/item/steps/item/summary")
    print("\nsummaries: ")
    for summary in summaries:
        print(summary.text)

    steps = root.findall("./app/sections/item/methods/item/steps/item/html")
    print("\nsteps: ")
    for step in steps:
        print(remove_HTML_and_citations(step.text))
        print ("\n")
        #dom = parseString(xml_page)
    #pretty = dom.toprettyxml()
    #f = open(title+".txt", "w", encoding="utf-8")
    #f.write(pretty)
    #f.close()