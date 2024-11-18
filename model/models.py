import random
from transformers import pipeline


# Dummy model for conducting initial test
class DummyModel:
    def __init__(self, topics):
        self.topics = topics

    def predict(self, text):
        # Generate random probabilities
        probabilities = [random.random() for _ in self.topics]
        total = sum(probabilities)
        normalized_probabilities = {topic: prob / total for topic, prob in zip(self.topics, probabilities)}
        return normalized_probabilities
    

    
class TransformerModel:
    def __init__(self, topics):
        self.topics = topics

    def predict(self, text):
       # Load zero-shot-classification pipeline
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

        result = classifier(text, self.topics)
        return result
    
    def analyze_sentiment(self, text):
        # Load text-classification pipeline with distil-bert model
        sentiment_analyzer = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        
        result = sentiment_analyzer(text)[0]

        return {"label": result['label'], "score": round(result['score'], 3)} 

    

