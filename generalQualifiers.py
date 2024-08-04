"""
This file is for looking at the data for a multiple player and their qualifer data.
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

    for eachMap in match:
        getBeatmap = requests.get(beatmapUrl + eachMap['beatmap_id']).json()
        beatmap = getBeatmap[0]['title']

        for score in eachMap['scores']:
            if score['user_id'] not in playerIDs:
                playerIDs.append(score['user_id'])
                getUsername = requests.get(userUrl + str(score['user_id'])).json()
                usernames.append(getUsername[0]['username'])
                matchScores[getUsername[0]['username']] = []

        hits = (300 * int(score['count300'])) + (100 * int(score['count100'])) + (50 * int(score['count50']))
        totalCombo = 300 * (int(score['count300']) + int(score['count100']) + int(score['count50']) + int(score['countmiss']))
        acc = round((hits / totalCombo) * 100, 2)
        matchScores[usernames[0]].append(([beatmap, acc]))

    return matchScores


if __name__ == "__main__":
    id = int(input("Enter mp link ID: "))
    result = getMpData(id)
    # print(data)
    # outputFileName = next(iter(data))
    # with open('qualifiers.json', 'w') as file:
    #     json.dump(data, file)

    with open('qualifiers.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

    # Append the new data
    if next(iter(result)) != "minatoaqua1":
        data[next(iter(result))] = result[next(iter(result))]
    else:
        data["balls"] = result[next(iter(result))]

    # Write the updated data back to the file
    with open('qualifiers.json', 'w') as file:
        json.dump(data, file, indent=4)
