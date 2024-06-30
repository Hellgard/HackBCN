 ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################


import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# put a variable in the local storage, if the variable already exists, it will be overwritten
def setLocalData(key, value):
    with open('local_storage.txt', 'r') as file:
        lines = file.readlines()
    bool = False
    with open('local_storage.txt', 'w') as file:
        for line in lines:
            if key in line:
                file.write(f'{key}:::{value}\n')
                bool = True
            else:
                file.write(line)
        if not bool:
            file.write(f'{key}:::{value}\n')
       

# get a variable from the local storage
def getLocalData(key):
    with open('local_storage.txt', 'r') as file:
        for line in file:
            if key in line:
                return line.split(":::")[1].replace("\n", "")
    return None
  
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

# Download NLTK tokenizer data for Spanish
nltk.download('punkt')

def summarize_text(text, max_length):
    parser = PlaintextParser.from_string(text, Tokenizer('spanish'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, max_length)
    return ' '.join([str(sentence) for sentence in summary])

def extract_and_summarize(url, max_length=50):
    print("Extracting and summarizing text from URL...")
    print(url)
    url = url.replace('https://', 'http://')  # Avoid SSL certificate issues
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
   
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        print("href is: " + str(href))
        if href:
            links.append(href)


    all_text = ''
    for paragraph in soup.find_all('p'):
        all_text += paragraph.get_text() + '\n'

    if len(all_text) > 500:
        summarized_text = summarize_text(all_text, max_length)
    else:
        summarized_text = all_text

    return summarized_text, links

# # Example usage:
# url = 'https://es.wikipedia.org/wiki/Napole%C3%B3n_Bonaparte'
# summarized_text, links = extract_and_summarize(url)

# print("Summarized text:")
# print(summarized_text)

# print("\nList of links:")
# for link in links:
#     print(link)
