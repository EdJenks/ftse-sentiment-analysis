import csv
from datetime import datetime
from classification_model import compute_article_sentiment_score
from data_collection import get_company_news
from collect_companies import scrape_ftse_100_companies

today = datetime.today().strftime('%Y-%m-%d')

# Set this to True for first run, False after
GET_FTSE_COMPANIES = False

def main(days_ago = 30, get_ftse_companies = GET_FTSE_COMPANIES, max_articles = 100):

    # One time call to save the ftse100 companies and tickers locally
    if get_ftse_companies:
        scrape_ftse_100_companies()

    # Read the list of companies
    with open('companies.txt', 'r') as companies_file:
        companies = companies_file.read().splitlines()
    
    # Loop through the companies and for each write its sentiment score to csv file
    with open('scores.csv', 'w', newline='') as scores_file:
            csv_writer = csv.writer(scores_file)
            csv_writer.writerow(['Company', 'Ticker', 'sentiment_vector', 'date', 'days_search_window'])

            for company in companies:
                # Get name and ticker
                company_name, ticker = company.split(',')

                # Get articles from API
                # get_company_news(ticker = ticker, company_name = company_name, num_articles = max_articles, days_ago=days_ago)

                # Get single sentiment vector/softmax score
                score = compute_article_sentiment_score(ticker)

                # Save score 
                csv_writer.writerow([company_name, ticker, score, today, days_ago])

if __name__ == '__main__':
    main()