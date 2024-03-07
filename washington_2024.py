import requests
import sys
from bs4 import BeautifulSoup
import time

LIST_URL = 'https://data.wa.gov/resource/3h9x-7bvm.json?$query=select%20filer_name%20as%20filer_name%2Celection_year%20as%20election_year%2Cjurisdiction%20as%20jurisdiction%2Coffice%20as%20office%2Cposition%20as%20position%2Cparty%20as%20party%2Ccase(contributions_amount%20is%20null%2C%200%2C%20true%2C%20contributions_amount)%20as%20contributions_amount%2Ccase(expenditures_amount%20is%20null%2C%200%2C%20true%2C%20expenditures_amount)%20as%20expenditures_amount%2Ccase(debts_amount%20is%20null%2C%200%2C%20true%2C%20debts_amount)%20as%20debts_amount%2Ccase(independent_expenditures_for_amount%20is%20null%2C%200%2C%20true%2C%20independent_expenditures_for_amount)%20as%20independent_expenditures_for_amount%2Ccase(independent_expenditures_against_amount%20is%20null%2C%200%2C%20true%2C%20independent_expenditures_against_amount)%20as%20independent_expenditures_against_amount%2Cjurisdiction_type%20as%20jurisdiction_type%2Ccandidacy_id%2Cjurisdiction_code%20as%20jurisdiction_code%20where%20political_committee_type%20%3D%20%22Candidate%22%20%20and%20election_year%20%3D%202024%20order%20by%20filer_name%20asc%2Celection_year%20desc%2C%3Aid%20limit%2050%20offset%200'
LIMIT = 50
OFFSET_PARAM = '%20offset%20'
TOTAL_CANDIDATES = 3000

CANDIDATE_URL = 'https://www.pdc.wa.gov/political-disclosure-reporting-data/browse-search-data/candidates/'

def get_list_url(offset):
    if (offset == 0):
        return LIST_URL + str(LIMIT)
    else:
        return LIST_URL + str(LIMIT) + OFFSET_PARAM + str(offset * LIMIT)

def download_candidate(candidate_id):
    can_page = requests.get(CANDIDATE_URL + candidate_id)
    soup = BeautifulSoup(can_page.text, 'html.parser')
    email_title = soup.find('h3', text='Email:')
    if email_title:
        print(email_title.next_sibling.strip())
    else:
        print('Couldn\'t find email for candidate %s' % candidate_id)
    time.sleep(.1) # slight delay to avoid blocking

def download_list(offset):
    url = get_list_url(offset)
    #print('downloading list: ' + url)
    list_page = requests.get(url).json()
    for candidate in list_page:
        download_candidate(candidate['candidacy_id'])

def main(argv):
    for i in range(int(TOTAL_CANDIDATES / LIMIT)):
        download_list(i)

if __name__ == '__main__':
    main(sys.argv[1:])
