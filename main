__author__ = 'stephenlechner'

# This program will collect the latest filed (forms 3,4,5) director non-
# derivative security ownership numbers for a list of companies (by ticker).
#
# This data will be outputted in separate csvs for each company, named by
# ticker.
#
# For starters, we will use the S&P 500 for the purposes of adding this data
# automatically to the issuer scorecard inputs (first round, due 12/1/2015).
#
# TODO: add the correct filepaths for (1) your csv that contains the list
# of tickers you're interested in collecting data for, and (2) the filepath
# for the desired destination of the result-csvs. 

import csv
import funcs
import timeit


# define the company list. referring to a csv with a list of tickers in the
# first column.
tic_list = []
# TODO: change the filing path below for the csv that contains the list of
# tickers for which you want to search for data
with open(
        '***ADD YOUR TICKER LIST FILEPATH HERE***', 'rU'
) as sp_doc:
    sp_read = csv.reader(sp_doc)
    for line in sp_read:
        tic_list.append(line[0])
start = timeit.default_timer()
i = 0
get_file = True
for tkr in tic_list:
    # some tickers have '/' in them, usually when its for a stock that has
    # multiple classes. E.g, BF/A. I haven't yet figured out how to correctly
    # account for this.
    tkr = tkr.replace('/', '-')
    # TODO: add the folder path for your data destination in the line below
    file_name = str(
        '***ADD YOUR DESTINATION FILEPATH HERE***' + tkr + '.csv'
    )
    # # if you want to stop from re-searching data for files you already have
    # # in the directory, then uncomment these lines.
    # if os.path.isfile(file_name) is False:
    #     get_file = True
    # else:
    #     get_file = False
    if get_file is True:
        i += 1
        # status update. includes the time it took to collect the last data
        print str(i), tkr, str(timeit.default_timer() - start)
        start = timeit.default_timer()
        dir_data_list = []
        dir_data = funcs.get_all_directors_own_data(tkr)  # returns dictionary
        # {"LAST First Name": "### of shares", ...} but it will need sorting.
        for dat in dir_data:
            dir_data_list.append((dat, dir_data[dat]))
        dir_data_list.sort()

        with open(file_name, 'wb') as write_doc:
            doc_write = csv.writer(write_doc)
            for each in dir_data_list:
                doc_write.writerow(each)
