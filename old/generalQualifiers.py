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
            matchScores[getUsername[0]['username']] = {}

        player = usernames[playerIDs.index(score['user_id'])]
        hits = (300 * int(score['count300'])) + (100 * int(score['count100'])) + (50 * int(score['count50']))
        totalCombo = 300 * (int(score['count300']) + int(score['count100']) + int(score['count50']) + int(score['countmiss']))
        acc = round((hits / totalCombo) * 100, 2)

        matchScores[player][beatmap] = acc

#   beatmapArray = matchScores[0]
#   condensedMatchScores = [beatmapArray]
#   matchScores.pop(0)

#   for playerScores in matchScores:
#     condensedPlayerScores = [playerScores[0]]
#     beatmapIndex = 1

#     for acc, beatmap in playerScores[1:]:
#       while beatmapArray[beatmapIndex] != beatmap:
#         condensedPlayerScores.append(-1)
#         beatmapIndex += 1
#       condensedPlayerScores.append(acc)
#       beatmapIndex += 1

#     while beatmapIndex < len(beatmapArray):
#       condensedPlayerScores.append(-1)
#       beatmapIndex += 1

#     condensedMatchScores.append(condensedPlayerScores)

  return usernames, matchScores


if __name__ == "__main__":
    id = int(input("Enter mp link ID: "))
    players, result = getMpData(id)
    # print(data)
    # outputFileName = next(iter(data))t
    with open('qualifiers2.json', 'w') as file:
        json.dump(result, file)

    # print(players, result)

    # if os.path.exists('qualifiers2.json'):
    #     with open('qualifiers2.json', 'r') as file:
    #         try:
    #             data = json.load(file)
    #         except json.JSONDecodeError:
    #             data = []
    # else:
    #     data = []

    # # Append the new data

    # data[next(iter(result))] = result[next(iter(result))]


    # # Write the updated data back to the file
    # with open('qualifiers2.json', 'w') as file:
    #     json.dump(data, file, indent=4)
