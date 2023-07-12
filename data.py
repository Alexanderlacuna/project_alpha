"""
making post request:
https://odibets.com/api/fvss
data 
{
    "competition_id": "1",
    "tab": "",
    "period": "2023-06-27 21:42:00"
}

"""
import os
import requests
import json
def fetch_odds():
    response = requests.get("https://odibets.com/api/fv")
    data = response.json()["data"]
    match_start_time = ""
    results = {}
    for (index,match) in enumerate(data["matches"],1):
        parent_id = match["parent_match_id"]
        outcomes = match["outcomes"]
        # looking for home,draw,away odds
        meta = {}
        match_start_time = match["start_time"]

        other_meta = {
         "start_time":match["start_time"],
         "home_team":match["home_team"],
         "away_team":match["away_team"]

        }

        for outcome in outcomes:
            if outcome["sub_type_id"] == "1X2":

                if outcome["outcome_key"] == '1':
                    meta["home_odds"] =  outcome["odd_value"]
                elif  outcome["outcome_key"] == 'X':
                    meta["draw_odds"] =  outcome["odd_value"]

                elif outcome["outcome_key"] == "2":
                    meta["away_odds"] = outcome["odd_value"]


        if meta:
            meta["parent_match_id"] = parent_id
            meta["position"] = index
            meta["other"] = other_meta
            results[parent_id] = meta

    if results:
        return {match_start_time:results}



def write_to_file(meta):
    old = {}
    try:
        with open(os.path.join(os.getcwd(),"data","data.txt")) as user_file:
            parsed_json = json.load(user_file)
            if parsed_json:
                old = parsed_json
    except Exception as e:
        pass
    with open(os.path.join(os.getcwd(),"data","data.txt"), "w+") as outfile:
        json.dump({**old,**meta}, outfile)
import schedule
import time

def job():
    results = fetch_odds()
    if results:
        write_to_file(results)
        print("written to file>>>>>>>>>>")

schedule.every(30).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)

