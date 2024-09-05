from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from textblob import TextBlob

app = Flask(__name__)

def analyze_sentiment(tweet):
    # Function to perform sentiment analysis using TextBlob
    if not isinstance(tweet, str):
        return "unknown" 
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        return "strongly positive"
    elif polarity > 0.0:
        return "weakly positive"
    elif polarity < -0.3:
        return "strongly negative"
    elif polarity < 0.0:
        return "weakly negative"
    else:
        return "neutral"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index2'))

    return render_template('index.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return "No file part"
        
        file = request.files['csv_file']
        if file.filename == '':
            return "No selected file"

        if file:
            tweets_df = pd.read_csv(file)
            tweets = tweets_df['tweet'].tolist()

            # Analyze the sentiment of the provided tweets and categorize them
            sentiment_categories = [analyze_sentiment(tweet) for tweet in tweets]

            # Calculate the percentage of each sentiment category
            total_tweets = len(tweets)
            sentiment_categories.count("strongly positive")
            a=sentiment_categories.count("strongly positive") 
            b=sentiment_categories.count("weakly positive")
            c= sentiment_categories.count("strongly negative")
            d=sentiment_categories.count("weakly negative") 
            e=sentiment_categories.count("neutral")
            strongly_positive_percentage = a/ total_tweets * 100
            weakly_positive_percentage = b / total_tweets * 100
            strongly_negative_percentage = c / total_tweets * 100
            weakly_negative_percentage = d / total_tweets * 100
            neutral_percentage = e/ total_tweets * 100

            return render_template('result.html',
                                   total_tweets=total_tweets,a=a,b=b,c=c,d=d,e=e,
                                   strongly_positive_percentage=strongly_positive_percentage,
                                   weakly_positive_percentage=weakly_positive_percentage,
                                   strongly_negative_percentage=strongly_negative_percentage,
                                   weakly_negative_percentage=weakly_negative_percentage,
                                   neutral_percentage=neutral_percentage
                                   )

    return render_template('index2.html')


@app.route('/sample')
def sample():
    return render_template('sample.html')

app.run(debug=True)