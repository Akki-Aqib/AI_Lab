"""
Sentiment Analysis & Polarity Detection
Rule-based + VADER-style lexicon approach (no external ML needed)
"""

# Simple sentiment lexicon
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love',
    'best', 'awesome', 'happy', 'brilliant', 'perfect', 'beautiful', 'nice',
    'superb', 'outstanding', 'joy', 'positive', 'liked', 'enjoy', 'pleasant',
    'delightful', 'impressive', 'fabulous', 'magnificent', 'terrific', 'glad'
}
NEGATIVE_WORDS = {
    'bad', 'terrible', 'horrible', 'awful', 'worst', 'hate', 'ugly', 'poor',
    'disappointing', 'sad', 'miserable', 'dreadful', 'pathetic', 'disgusting',
    'annoying', 'boring', 'useless', 'negative', 'failure', 'disaster', 'nasty',
    'broken', 'slow', 'painful', 'frustrating', 'angry', 'waste', 'wrong'
}
NEGATIONS     = {'not', 'no', 'never', "n't", 'neither', 'nobody', 'nothing'}
INTENSIFIERS  = {'very', 'extremely', 'really', 'absolutely', 'totally', 'so', 'quite'}

def analyze_sentiment(text):
    words = text.lower().split()
    score = 0
    i = 0
    while i < len(words):
        word = words[i].strip(".,!?;:'\"")
        # Check negation in window
        negated = any(words[max(0,i-j)].strip(".,!?") in NEGATIONS for j in range(1,4))
        # Check intensifier
        intensity = 2.0 if (i > 0 and words[i-1].strip(".,!?") in INTENSIFIERS) else 1.0
        if word in POSITIVE_WORDS:
            score += -intensity if negated else intensity
        elif word in NEGATIVE_WORDS:
            score += intensity if negated else -intensity
        i += 1

    # Normalize to [-1, 1]
    word_count = len(words) or 1
    polarity = max(-1.0, min(1.0, score / (word_count ** 0.5)))

    if polarity > 0.2:
        sentiment = "POSITIVE 😊"
    elif polarity < -0.2:
        sentiment = "NEGATIVE 😞"
    else:
        sentiment = "NEUTRAL 😐"

    return {
        'text': text,
        'polarity': round(polarity, 3),
        'sentiment': sentiment,
        'raw_score': score
    }

def batch_analyze(texts):
    print("=" * 60)
    print("      Sentiment Analysis & Polarity Detection")
    print("=" * 60)
    for text in texts:
        result = analyze_sentiment(text)
        print(f"\nText     : {result['text']}")
        print(f"Polarity : {result['polarity']:+.3f}  |  {result['sentiment']}")
    print("=" * 60)

if __name__ == "__main__":
    test_texts = [
        "This product is absolutely amazing and wonderful!",
        "The movie was terrible and boring. I hated it.",
        "It was okay, not very good but not bad either.",
        "I really love this place. The food is excellent!",
        "This is not bad at all, actually quite good.",
        "Worst experience ever. Very disappointing service.",
        "The weather is fine today.",
        "I am extremely happy with the results!",
    ]
    batch_analyze(test_texts)
