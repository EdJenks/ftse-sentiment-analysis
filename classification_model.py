from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import pandas as pd
from text_preprocessing import preprocess_text

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = BertForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

# Create financial BERT sentiment analysis pipeline
finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

sentiment_vector_coefficient = {'Negative': -1, 'Positive': 1, 'Neutral': 0}

def compute_article_sentiment_score(ticker):
    # Read article data received from API
    file_path = f'./data/{ticker}_news_data.json'
    df = pd.read_json(file_path)

    # Sometimes there won't be any articles for a company
    if not df.empty:

        # Combine title and description to perform sentiment analysis on all at once
        combined_text = df[['title', 'description']].apply(lambda x: ' '.join(x.dropna()), axis=1).to_list()
        combined_text_cleaned = [' '.join(preprocess_text(article)) for article in combined_text]

        # Get sentiment score of each article and save to df
        sentiment_score = finbert(combined_text_cleaned)
        df['sentiment_label'] = [x['label'] for x in sentiment_score]
        df['sentiment_probabolity'] = [x['score'] for x in sentiment_score]
        df['sentiment_vector'] = [x['score'] * sentiment_vector_coefficient[x['label']] for x in sentiment_score]

        # Save data now with scores
        df.to_json(file_path, orient = 'records' , indent=4)

        # Calculate sentiment vector score for company
        sentiment_vector_score = df['sentiment_vector'].mean()

        return sentiment_vector_score