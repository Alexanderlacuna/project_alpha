"""
we need huge data for this
"""

def write_to_file(meta):
    with open(os.path.join(os.getcwd(),"data","JUNE-monthly.txt"), "w+") as outfile:
        json.dump({"meta":meta}, outfile)





def fetch_results(timestamp=None,competition_id=1):
    response = requests.get(f"https://vl.odi.life/fvs?competition_id=1&period={timestamp}")
    results = response.json()
    return results["data"]["matches"]


results = []
init_date = "2023-06-07+04:02:00"
import datetime
import requests
import json
import os
from datetime import timedelta
meta =  []


all_timers = []

while datetime.datetime.now() > datetime.datetime.strptime(init_date, '%Y-%m-%d+%H:%M:%S'):
    all_timers.append(init_date)
    datetime_object = datetime.datetime.strptime(init_date, '%Y-%m-%d+%H:%M:%S')
    result = datetime_object+ timedelta(minutes=2)
    init_date = result.strftime('%Y-%m-%d+%H:%M:%S')

"""
while datetime.datetime.now() > datetime.datetime.strptime(init_date, '%Y-%m-%d+%H:%M:%S'):

    result = fetch_results(init_date)
    datetime_object = datetime.datetime.strptime(init_date, '%Y-%m-%d+%H:%M:%S')
    print("fetching for date >>>>>>>>>>>>>>>>>>>>>>>>>>",datetime_object)
    rk = fetch_results(init_date)
    meta.insert(0,rk)

    result = datetime_object + timedelta(minutes=2)
    init_date = result.strftime('%Y-%m-%d+%H:%M:%S')
"""

import requests
import multiprocessing
import time

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")



def fetch_sites(timestamp=None):
    response = session.get(f"https://vl.odi.life/fvs?competition_id=1&period={timestamp}",verify=False)
    results = response.json()
    return results["data"]["matches"]


def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        return pool.map(fetch_sites, sites)



def generate_hashes():
    hashes = []
    with open(os.path.join(os.getcwd(),"data","JUNE-monthly.txt")) as file_handler:
        parsed_json = json.load(file_handler)

        for occurence in parsed_json["meta"]:
            team_matches = []
            for match in occurence:
                team_names = "".join(match["home_team"].split(" ")).lower() +"".join(match["away_team"].split(" ")).lower()
                team_matches.append(team_names)

            hashes.append(get_list_hash(team_matches))

    return hashes

import hashlib

def get_list_hash(lst):
    # Sort the list to ensure similar lists have the same hash
    # Join the sorted list elements into a single string
    joined_str = ''.join(lst)
    hash_obj = hashlib.md5()
    hash_obj.update(joined_str.encode('utf-8'))
    hash_value = hash_obj.hexdigest()
    return hash_value



from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

HASHES = generate_hashes()
def check_for_hash(timer):

    results = generate_hashes()
    response = requests.get(f"https://vl.odi.life/fvs?competition_id=1&period={timer}", verify=False)
    matches = response.json()["data"]["matches"]

    new_hash = []
    for match in matches:
        team_names = "".join(match["home_team"].split(" ")).lower() +"".join(match["away_team"].split(" ")).lower()
        new_hash.append(team_names)

    if get_list_hash(new_hash) in HASHES and new_hash!=[]:

        raise Exception
        print("found hash found hash found>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",new_hash)

from datetime import datetime,timedelta

init_date = "2023-07-12+04:42:00"

while True:
    res = "+".join(str(datetime.now()+ timedelta(minutes=1)).split(" "))
    res = "+".join(res.split(".")[0])

    datetime_object = datetime.strptime(init_date, '%Y-%m-%d+%H:%M:%S')
    print("checking hash for >>>>>>>>>>>>>>>>>>>>>>>>>>",datetime_object)
    check_for_hash(init_date)
    result = datetime_object + timedelta(minutes=1)
    init_date = result.strftime('%Y-%m-%d+%H:%M:%S')

'''

if __name__ == "__main__":
    start_time = time.time()
    results = download_all_sites(all_timers)
    duration = time.time() - start_time
    print(f"Downloaded  in {duration} seconds")
    write_to_file(results)
    exit()
'''





