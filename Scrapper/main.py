import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Download NLTK tokenizer data for Spanish
nltk.download('punkt')

# Function to summarize text to a maximum length
def summarize_text(text, max_length=50):
    parser = PlaintextParser.from_string(text, Tokenizer('spanish'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, max_length)
    return ' '.join([str(sentence) for sentence in summary])

url = 'https://es.wikipedia.org/wiki/Napole%C3%B3n_Bonaparte'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract and print all links
print("List of links:")
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.startswith('http'):  # Filter out non-HTTP links
        print(href)

# Extract and print all text
print("\nAll text content:")
all_text = ''
for paragraph in soup.find_all('p'):
    all_text += paragraph.get_text() + '\n'

# Summarize if necessary
if len(all_text) > 500:
    summarized_text = summarize_text(all_text)
    print(summarized_text)
else:
    print(all_text)
