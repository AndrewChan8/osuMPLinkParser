"""
This file is for looking at the data for a single player and their qualifer data.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv('apiKey')

def getMpData(mpLink):
    matchUrl = f"https://osu.ppy.sh/api/get_match?k={apiKey}&mp={mpLink}"
    userUrl = f"https://osu.ppy.sh/api/get_user?k={apiKey}&u="
    beatmapUrl = f"https://osu.ppy.sh/api/get_beatmaps?k={apiKey}&b="

    getMatch = requests.get(matchUrl).json()
    match = getMatch['games']
    playerIDs = []
    usernames = []
    matchScores = {}
    beatmaps = []

    for eachMap in match:
        getBeatmap = requests.get(beatmapUrl + eachMap['beatmap_id']).json()
        beatmap = getBeatmap[0]['title']
        beatmaps.append(beatmap)

        for score in eachMap['scores']:
            if score['user_id'] not in playerIDs:
                playerIDs.append(score['user_id'])
                getUsername = requests.get(userUrl + str(score['user_id'])).json()
                usernames.append(getUsername[0]['username'])
                matchScores[getUsername[0]['username']] = {}

        hits = (300 * int(score['count300'])) + (100 * int(score['count100'])) + (50 * int(score['count50']))
        totalCombo = 300 * (int(score['count300']) + int(score['count100']) + int(score['count50']) + int(score['countmiss']))
        acc = round((hits / totalCombo) * 100, 2)
        matchScores[getUsername[0]['username']][beatmap] = acc

    return beatmaps, matchScores


if __name__ == "__main__":
    mpLinks = []

    print("Enter multiplayer lobby IDs.")
    print("Note: If you want to enter multiple at a time, seperate the IDs with spaces")
    print("To finish, enter 0 (zero)")
    while True:
        id = input("Enter mp link IDs: ")
        idList = id.split()
        if '0' in idList:
            break
        idList = [int(id) for id in idList]
        if len(idList) > 1:
            mpLinks += idList
        else:
            mpLinks.append(id)


    for link in mpLinks:
        beatmaps, results = getMpData(link)

        if not os.path.exists('qualifiers.json'):
            with open('qualifiers.json', 'w') as file:
                json.dump({}, file)

        with open('qualifiers.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

        # Append the new data
        if "beatmaps" not in data:
            data["beatmaps"] = beatmaps
        data[next(iter(results))] = results[next(iter(results))]
        data[next(iter(results))]['mpLink'] = link

        # Write the updated data back to the file
        with open('qualifiers.json', 'w') as file:
            json.dump(data, file, indent=4)
