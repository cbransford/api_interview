import requests
from collections import defaultdict
import heapq
from operator import itemgetter
import math
class3_url = "https://api.fda.gov/food/enforcement.json?search=classification:\"Class+III\""
all_year_url = "https://api.fda.gov/food/enforcement.json?search=report_date[{year}0101+TO+{year}1231]"

state_codes = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

def get_number_of_records(url):
    response = requests.get(url).json()
    return response["meta"]["results"]["total"]

def get_all_records(url, num_records):
    pages = math.ceil(num_records / 1000)
    records = []
    for i in range(pages):
        formatted_url = url + "&limit=1000&skip=" + str(i*1000)
        response = requests.get(formatted_url).json()["results"]
        records.extend(response)
    return records


def get_state_status_code_counts(responses):
    counts = defaultdict(int)
    for response in responses:
        counts["State " + response["state"] +"/Status " + response["status"]] += 1

    return heapq.nlargest(10, counts.items(), key=itemgetter(1))

def get_state_counts(responses):
    counts = defaultdict(int)
    for response in responses:
        counts[response["state"]] += 1

    return heapq.nlargest(10, counts.items(), key=itemgetter(1))





if __name__ == '__main__':
    num_recs = get_number_of_records(class3_url)
    class3_results = get_all_records(class3_url, num_recs)
    top10_state_codes = get_state_status_code_counts(class3_results)
    print("----")
    for item in map(lambda s: s[0] + ": " + str(s[1]), top10_state_codes):
        print(item)

    print("----")
    all_2016_url= all_year_url.format(year=2016)
    avg_2016_records = get_number_of_records(all_2016_url) / 12
    print(str(int(avg_2016_records)) + " reports")
    print("----")
    all_2017_url = all_year_url.format(year=2017)
    number_2017_recs = get_number_of_records(all_2017_url)
    results_2017 = get_all_records(all_2017_url, number_2017_recs)
    top_states_2017 = get_state_counts(results_2017)
    for item in map(lambda s: s[0] + ": " + str(s[1]), top_states_2017):
        print(item)

    print("----")
    min_year = 2003
    max_year = 2003
    min_val = float('inf')
    max_val = float('-inf')
    for year in range(2004, 2021):
        count = get_number_of_records(all_year_url.format(year=year))
        if count < min_val:
            min_val = count
            min_year = year
        elif count > max_val:
            max_val = count
            max_year = year
    print(f"Highest year is {max_year} with {max_val} reports")
    print(f"Lowest year is {min_year} with {min_val} reports")

    print('----')
    for item in map(lambda s: state_codes[s[0]] + ": " + str(s[1]), top_states_2017):
        print(item)










