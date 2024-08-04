import json
import os

# Open the JSON file
with open('qualifiers.json', 'r') as file:
    results = json.load(file)

def extractPlayers(results):
    return list(results.keys())

def mapPlayersToScore(results):
    scores = {result: [] for result in results["beatmaps"]} # Make dict of beatmaps as the key and empty array as player scores
    del results["beatmaps"]

    for result in results:
        for score in results[result]:
            if score == 'mpLink':
                break
            scores[score].append((result, results[result][score]))

    return scores

def mapRanks(scores):
    for map in scores:
        scores[map] = sorted(scores[map], key=lambda x: x[1], reverse=True)

def calculateRankSum(scores):
    playerRankSum = {}
    playerLowestRanks = {}
    for score in scores:
        for rank in range(len(scores[score])):
            player = scores[score][rank][0]
            if player not in playerRankSum:
                playerRankSum[player] = 0
                playerLowestRanks[player] = 0
            playerRankSum[player] += rank + 1
            if playerLowestRanks[player] < rank + 1:
                playerLowestRanks[player] = rank + 1
    for player in playerRankSum:
        playerRankSum[player] = playerRankSum[player] - playerLowestRanks[player]
    
    sortedRankSum = dict(sorted(playerRankSum.items(), key=lambda item: item[1]))
    
    return sortedRankSum, playerLowestRanks

def sortRankSum(rankSum):
    return dict(sorted(rankSum.items(), key=lambda item: item[1]))

def printMpLinks(results):
    for player in results["mpLinks"]:
        print(results["mpLinks"][player], end=' ')
    print()

if __name__ == "__main__":
    mpLinks = {result: results[result]["mpLink"] for result in results if result != "beatmaps"}
    rankings = mapPlayersToScore(results)
    mapRanks(rankings)
    rankSum, lowest = calculateRankSum(rankings)

    results = {"mapRankings": rankings, "rankSum": rankSum, "playerLowestRanks": lowest, "mpLinks": mpLinks}

    if not os.path.exists('results.json'):
        with open('results.json', 'w') as file:
            json.dump({}, file)

    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)