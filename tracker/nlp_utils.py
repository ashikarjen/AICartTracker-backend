import spacy
import re

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_url(text):
    # Used regular expressions to find URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(text)
    return urls

def get_intent(text):
    # Simple keyword-based intent recognition
    if "track" in text.lower():
        return "track_product"
    else:
        return "unknown_intent"
