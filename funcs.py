__author__ = 'stephenlechner'

# This file contains the functions needed to scrape the latest director
# stock ownership of a company with a given ticker.

import requests
from bs4 import BeautifulSoup


class PageCont:
    # This class is effectively a home-made xml parser, specifically written
    # for (and therefore limited to) the contents of forms 3, 4, and 5.
    def __init__(self, the_text):
        self.text = the_text

    def tag(self, tag_name, remove_tags=False):
        # returns the content of the first of any given tag, if it exists.
        # can return with tags or without.
        if self.text.count('<' + tag_name + '>') == 0:
            return None
        tag_start = self.text.find('<' + tag_name + '>') + len(tag_name) + 2
        tag_end = self.text.find('</' + tag_name + '>')
        cont = self.text[tag_start:tag_end]
        if remove_tags is True:
            while cont.count('<') > 0 and cont.find('>') > cont.find('<'):
                cont = cont[:cont.find('<')] + cont[cont.find('>')+1:]
            cont = cont.replace('\n', ' ')
        return cont.strip()

    def rtag(self, tag_name, remove_tags=False):
        # returns the content of the last of any given tag, if it exists.
        # can return with tags or without.
        if self.text.count('<' + tag_name + '>') == 0:
            return None
        tag_start = self.text.rfind('<' + tag_name + '>') + len(tag_name) + 2
        tag_end = self.text.rfind('</' + tag_name + '>')
        cont = self.text[tag_start:tag_end]
        if remove_tags is True:
            while cont.count('<') > 0 and cont.find('>') > cont.find('<'):
                cont = cont[:cont.find('<')] + cont[cont.find('>')+1:]
            cont = cont.replace('\n', ' ')
        return cont.strip()

    def non_deriv_tag(self, tag_name):
        # returns teh content of the first of any given tag if it exists within
        # the 'nonDerivativeTable' tag (which holds the common stock updates
        # for the reported person--in this case directors).
        # returns content with tags removed.
        non_deriv_cont = self.tag('nonDerivativeTable')
        if non_deriv_cont is None:
            return None
        tag_start = non_deriv_cont.find('<' + tag_name + '>') + len(tag_name)+2
        tag_end = non_deriv_cont.find('</' + tag_name + '>')
        cont = non_deriv_cont[tag_start:tag_end]
        while cont.count('<') > 0 and cont.find('>') > cont.find('<'):
            cont = cont[:cont.find('<')] + cont[cont.find('>')+1:]
        cont = cont.replace('\n', ' ')
        return cont.strip()

    def r_non_deriv_tag(self, tag_name):
        # returns teh content of the last of any given tag if it exists within
        # the 'nonDerivativeTable' tag (which holds the common stock updates
        # for the reported person--in this case directors).
        # returns content with tags removed.
        non_deriv_cont = self.rtag('nonDerivativeTable')
        if non_deriv_cont is None:
            return None
        tag_start = non_deriv_cont.find('<' + tag_name + '>') + len(tag_name)+2
        tag_end = non_deriv_cont.find('</' + tag_name + '>')
        cont = non_deriv_cont[tag_start:tag_end]
        while cont.count('<') > 0 and cont.find('>') > cont.find('<'):
            cont = cont[:cont.find('<')] + cont[cont.find('>')+1:]
        cont = cont.replace('\n', ' ')
        return cont.strip()

    def deriv_tag(self, tag_name):
        # returns teh content of the first of any given tag if it exists within
        # the 'derivativeTable' tag (which holds e.g, option ownership updates
        # for the reported person--in this case directors).
        # returns content with tags removed.
        deriv_cont = self.tag('derivativeTable')
        if deriv_cont is None:
            return None
        tag_start = deriv_cont.find('<' + tag_name + '>') + len(tag_name)+2
        tag_end = deriv_cont.find('</' + tag_name + '>')
        cont = deriv_cont[tag_start:tag_end]
        while cont.count('<') > 0 and cont.find('>') > cont.find('<'):
            cont = cont[:cont.find('<')] + cont[cont.find('>')+1:]
        cont = cont.replace('\n', ' ')
        return cont.strip()

    def r_deriv_tag(self, tag_name):
        # returns teh content of the last of any given tag if it exists within
        # the 'derivativeTable' tag (which holds e.g, option ownership updates
        # for the reported person--in this case directors).
        # returns content with tags removed.
        deriv_cont = self.rtag('derivativeTable')
        if deriv_cont is None:
            return None
        tag_start = deriv_cont.find('<' + tag_name + '>') + len(tag_name)+2
        tag_end = deriv_cont.find('</' + tag_name + '>')
        cont = deriv_cont[tag_start:tag_end]
        while cont.count('<') > 0 and cont.find('>') > cont.find('<'):
            cont = cont[:cont.find('<')] + cont[cont.find('>')+1:]
        cont = cont.replace('\n', ' ')
        return cont.strip()


def get_own_search_page_cont(tic):
    # this function takes a ticker as a string, and uses it to search for the
    # last 100 available forms 3, 4, or 5 of the company. it returns the page
    # of the search results in the form of a Beautiful Soup object, if the
    # search results contain links to any forms 3,4, or 5.
    search_url = str(
        "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" +
        tic + "&dateb=&owner=only&count=100"
    )
    search_page = requests.get(search_url)
    search_page_text = search_page.text
    search_soup = BeautifulSoup(search_page_text)

    search_soup.find(id="seriesDiv")
    if search_soup.find(id="seriesDiv") is None:
        print tic, ": Did not get Edgar search results for this ticker."
        return None
    else:
        if search_soup.find(id='seriesDiv').a is None:
            print tic, ": Did not get Edgar search results for this ticker."
            return None
        else:
            return search_soup


def get_all_directors_own_data(tic):
    # this function takes a ticker as a string, and searches for the most
    # recent 100 forms 3, 4, or 5 filed by that ticker's company with the SEC.
    # it then searches through the xml (in .txt files) of all the forms found
    # and collects the number of shares owned by each director as of the last
    # form 3, 4, or 5 filed with their name. it returns this data in a
    # dictionary in order to efficiently exclude duplicate director data.
    dir_own_data = dict()
    # grabs initial search page and returns as a Beautiful Soup object, or None
    # if there are no form links in the search results.
    own_search_soup = get_own_search_page_cont(tic)
    if own_search_soup is not None:
        own_search_text = own_search_soup.get_text().lower()
        # the 'cik' is the Edgar system id for each company. it's necessary to
        # build the url for each file associated with the company searched.
        cik = own_search_text[own_search_text.find('cik#: ')+6:
                              own_search_text.find('cik#: ')+16]
        while cik[:1] == '0':  # must remove all first zeros
            cik = cik[1:]
        # the file-numbers are the last pieces missing to the file URLs.
        own_search_text = own_search_text[own_search_text.find("acc-no: ")+8:]
        own_linkstring_list = own_search_text.split('acc-no: ')
        for linkstring in own_linkstring_list:
            file_num = linkstring[:20]
            form_link = str(
                'http://www.sec.gov/Archives/edgar/data/' + cik + '/' +
                file_num.replace('-', '') + '/' + file_num + '.txt'
            )
            form_doc = requests.get(form_link)
            form_cont = PageCont(form_doc.text)
            # there will only be one 'rptOwnerName' and 'isDirector' tag in
            # each form. there may be many 'sharesOwnedFollowingTransaction',
            # but only the last found in the 'nonDerivativeTable' tag will be
            # of interest.
            filer_name = form_cont.tag('rptOwnerName')
            dir_status = form_cont.tag('isDirector')
            ending_shares = form_cont.r_non_deriv_tag(
                'sharesOwnedFollowingTransaction'
            )

            if dir_status is not None:
                if ((dir_status == '1' or dir_status.lower() == 'true')
                        and ending_shares is not None):
                    if filer_name not in dir_own_data:
                        dir_own_data[filer_name] = ending_shares
    return dir_own_data
