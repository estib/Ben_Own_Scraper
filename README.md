# Ben_Own_Scraper
This program will take a list of company tickers (as strings) and return the number of common stock owned by public company board directors found within the last 100 available filed Forms 3, 4, or 5.

To use, please download the "main.py" and "funcs.py" files for running (place them in the same directory). Create a csv that lists the tickers you would like to search data for, including only the tickers for each company in the first column of the csv. Then in "main.py" insert the filepaths for the ticker-list csv you created, and for the directory of where you would like the data results to be saved. Ensure that you are connected to the internet and that you have all the necessary libraries installed (itemized below). Then run "main.py".

The program will visit the last available 100 forms 3, 4, or 5 for each correct ticker privided in your csv. For any of these forms that were filed for a director, the program will grab the number of shares of common stock that that director owns as of the most recent form 3, 4, or 5 filed on behalf of that director by that company. For each company, it will create a csv that will list each director by name in alphabetical format (LAST First) and number of common shares owned.

This program relies on the following standard python libraries:
- csv
- timeit

It also relies on the following commonly used, but non-standard libraries:
- requests
- bs4 (only BeautifulSoup)
