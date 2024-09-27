from textblob import TextBlob
import re

def extract_url_from_command(command_text):
    url_regex = r'(https?://[^\s]+)'
    urls = re.findall(url_regex, command_text)
    return urls[0] if urls else None

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

def generate_product_summary(sentiments):
    total = len(sentiments)
    positive = sentiments.count('Positive')
    negative = sentiments.count('Negative')
    neutral = sentiments.count('Neutral')
    summary = f'Total Reviews: {total}\nPositive: {positive}\nNegative: {negative}\nNeutral: {neutral}'
    return summary
