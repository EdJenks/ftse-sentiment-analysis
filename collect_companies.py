import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/FTSE_100_Index'

def scrape_ftse_100_companies():

    # One time function to scrape the list of ftse100 companies
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('table', class_='wikitable sortable', id='constituents')

    # Write company names and tickers to txt file
    with open('companies.txt','w') as file:
        for row in table.find_all('tr')[1:]:
            company_name = row.findAll('td')[0].text
            ticker = row.findAll('td')[1].text
            file.write(f'{company_name},{ticker}\n')
    