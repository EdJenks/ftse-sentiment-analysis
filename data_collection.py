import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
# Personal news api key
API_KEY = os.getenv('API_KEY')

def get_company_news(ticker = 'shel', company_name = 'Shell Plc', num_articles = 100, days_ago = 30):
    date_from = (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    endpoint_url = f'https://newsapi.org/v2/everything?q={company_name}&pageSize={num_articles}&apiKey={API_KEY}&searchin=title&from={date_from}'
    response = requests.get(endpoint_url)
    print(response)
    articles = response.json().get('articles', [])

    # Prepare the folder and filename for saving the data
    folder_name = f'data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    file_name = f'{folder_name}/{ticker.lower()}_news_data.json'
    
    # Format and save data as JSON
    articles_data = []
    for article in articles:
        article_data = {
            'company': company_name,
            'ticker': ticker,
            'title': article['title'],
            'description': article['description'],
            'content': article['content'],
            'url': article['url'],
            'source': article['source']['name'],
            'published_at': article['publishedAt'],
            'collected_at': datetime.now(),
        }
        articles_data.append(article_data)
    
    with open(file_name, 'w') as json_file:
        json.dump(articles_data, json_file, indent=4, default=str)

    print(f'Saved {len(articles)} articles for {company_name} in {file_name}')
