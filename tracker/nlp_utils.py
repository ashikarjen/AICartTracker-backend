from textblob import TextBlob

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
