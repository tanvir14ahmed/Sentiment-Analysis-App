from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)

sia = SentimentIntensityAnalyzer()

def get_sentiment_label(sentence):
    sentiment = sia.polarity_scores(sentence)
    # Determine the sentiment label based on the compound score
    if sentiment['compound'] >= 0.05:
        return 'Positive'
    elif sentiment['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sentence = request.form['sentence']
        sentiment_label = get_sentiment_label(sentence)
        
        # MongoDB connection and insertion
        with pymongo.MongoClient('mongodb://localhost:27017/') as client:
            db = client['sentiment']
            collection = db['data']
            post = {"sentence": sentence, "sentiment": sentiment_label}
            post_id = collection.insert_one(post).inserted_id
        
        return render_template('index.html', sentence=sentence, sentiment=sentiment_label)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
