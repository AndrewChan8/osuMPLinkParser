def extractPlayers(results):
  return [result[0] if type(result[0]) is str else '' for result in results]

def mapPlayerToScore(players, results):
  playerScores = []
  for index, result in enumerate(results):
    if result[index] != players[index] and not index:
      return "Player is not the same as results"

    playerScoresMap = []
    for score in result:
      if type(score) is not str:
        playerScoresMap.append((players[index], score))
    
    playerScores.append(playerScoresMap)
  return playerScores

def mapRanks(playerScores):
  mapRankScore = []
  for index, score in enumerate(playerScores[0]):
    tempMapScore = []
    for i in range(len(playerScores)):
      tempMapScore.append(playerScores[i][index])
    sortedMapScore = sorted(tempMapScore, key=lambda x: x[1], reverse=True)
    mapRankScore.append(sortedMapScore)
  return mapRankScore

def calculateRankSum(rankScores):
  playerRankSum = {}
  playerLowestScores = {}
  for score in rankScores:
    for rank, playerScore in enumerate(score):
      if playerScore[0] not in playerRankSum:
        playerRankSum[playerScore[0]] = 0
        playerLowestScores[playerScore[0]] = 0
      playerRankSum[playerScore[0]] += rank + 1
      if playerLowestScores[playerScore[0]] < rank + 1:
        playerLowestScores[playerScore[0]] = rank + 1

    sortedRankSum = dict(sorted(playerRankSum.items(), key=lambda item: item[1]))
  return sortedRankSum, playerLowestScores

def removeLowestScores(rankSum, lowestScores):
  for player in rankSum:
    rankSum[player] -= lowestScores[player]