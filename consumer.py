import requests
import json
import os




def fetch_result(home,away,timer=0):

    with open(os.path.join(os.getcwd(),"data","results-2023-06-29 02:09:53.987863")) as file_handler:
        parsed_json = json.load(file_handler)

        team_full_name = "".join(home.split(" ")).lower() + "".join(away.split(" ")).lower()

        return {team_full_name:parsed_json.get(team_full_name)}

def fetch_specific(competition_id=1):
    response = requests.get(f"https://vl.odi.life/fvs?competition_id=1&period=2023-06-29+04:40:00")
    results = response.json()["data"]["matches"]
    response = {}
    for (index,match) in  enumerate(results,1):
        results_2 ={}
        results = fetch_result(match["home_team"],match["away_team"])
        #results_2  = fetch_result(match["away_team"],match["home_team"])


        data = []

        """

        for result in results.values():
            for val in  result:

                if val["position"] == index:
                    data.append(val)

        we = list(results.keys())
        results = {we[0]:data}

        """

        print("index>>>>>>>>>>>>>>>>>>>>",index)
        print(results)



        #print(">>>>>>>>>>>>>>>>>>>>results2")
        #print(results_2)


        response = {**response,**{**results_2,**results}}

    return response


import hashlib

def get_list_hash(lst):
    # Sort the list to ensure similar lists have the same hash
    # Join the sorted list elements into a single string
    joined_str = ''.join(lst)
    hash_obj = hashlib.md5()
    hash_obj.update(joined_str.encode('utf-8'))
    hash_value = hash_obj.hexdigest()
    return hash_value


def generate_hashes():
    hashes = []
    with open(os.path.join(os.getcwd(),"data","data2.txt")) as file_handler:
        parsed_json = json.load(file_handler)
        for (timestamp,data) in  parsed_json.items():
            current_date_match = []
            for (unique_match_id) in data.keys():
                match = data[unique_match_id]["other"]
                team_names = "".join(match["home_team"].split(" ")).lower() +"".join(match["away_team"].split(" ")).lower()
                current_date_match.append(team_names)

            hash_val = get_list_hash(current_date_match)
            hashes.append(hash_val)
    return hashes




HASHES = generate_hashes()
def check_for_hash(timer):

    results = generate_hashes()
    response = requests.get(f"https://vl.odi.life/fvs?competition_id=1&period={timer}")
    matches = response.json()["data"]["matches"]

    new_hash = []
    for match in matches:
        team_names = "".join(match["home_team"].split(" ")).lower() +"".join(match["away_team"].split(" ")).lower()
        new_hash.append(team_names)

    if get_list_hash(new_hash) in HASHES:
        print("found hash found hash found>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",new_hash)



import schedule
import time
from datetime import datetime, timedelta



init_date = "2023-07-03+23:24:00"
while True:
    res = "+".join(str(datetime.now()+ timedelta(minutes=1)).split(" "))
    res = "+".join(res.split(".")[0])

    datetime_object = datetime.strptime(init_date, '%Y-%m-%d+%H:%M:%S')
    print("checking hash for >>>>>>>>>>>>>>>>>>>>>>>>>>",datetime_object)
    check_for_hash(init_date)
    result = datetime_object + timedelta(minutes=1)
    init_date = result.strftime('%Y-%m-%d+%H:%M:%S')