import json

from qualifiers import getMpData
from rankSum import extractPlayers, mapPlayerToScore, mapRanks, calculateRankSum, removeLowestScores

def calculateAll(mpID):
    results = getMpData(mpID) # Get the mp link results
    beatmaps = results.pop(0) # Remove the beatmap listing
    players = extractPlayers(results) 

    playerScores = mapPlayerToScore(players, results)

    rankScores = mapRanks(playerScores)

    rankSum, lowestScores = calculateRankSum(rankScores)

    removeLowestScores(rankSum, lowestScores)
    return rankSum

if __name__ == "__main__":
    id = int(input("Enter the mp link ID: "))
    results = calculateAll(id)
    with open(f'{next(iter(results))}.json', 'w') as file:
        json.dump(results, file)

    # calculateAll(114349636)