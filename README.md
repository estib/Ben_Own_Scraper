# Ben_Own_Scraper
This program will take a list of company tickers (as strings) and return the number of common stock owned by public company board directors found within the last 100 available filed Forms 3, 4, or 5.

import requests
from bs4 import BeautifulSoup
