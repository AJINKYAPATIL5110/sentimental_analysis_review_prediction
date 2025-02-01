from textblob import TextBlob

def analyze_sentiment(review_text: str):
    """Analyze the sentiment of the given review text."""
    analysis = TextBlob(review_text)
    sentiment = "neutral"
    confidence_score = analysis.sentiment.polarity

    if confidence_score > 0:
        sentiment = "positive"
    elif confidence_score < 0:
        sentiment = "negative"

    return sentiment, confidence_score

# Test the function
review_text = "I love this product, it's amazing!"
sentiment, confidence_score = analyze_sentiment(review_text)
print(f"Sentiment: {sentiment}, Confidence Score: {confidence_score}")
