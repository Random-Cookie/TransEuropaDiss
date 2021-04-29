from Players.Bots.BasicBots import *
from TransEuropa import TransEuropa
import matplotlib.pyplot as plt

players = [ClosestFirst("Closest First"), FarthestFirst("Farthest First")]
map_filepath = "Structure/Maps/classic.txt"

no_games = 10000
games_won = [0] * len(players)
invalid_games = 0
for i in range(0, no_games):
	print("----------Game " + str(i) + "----------")
	game = TransEuropa(players, map_filepath, 1, 0)
	game.play_game()
	if game.turn_count == game.MAX_TURNS:
		invalid_games += 1
	for j in range(0, len(players)):
		if players[j].has_won():
			games_won[j] += 1
		players[j].reset()

fig = plt.figure()
player_names = []
for player in players:
	player_names.append(player.name)
player_names.append("Draws")
games_won.append((games_won[0] + games_won[1]) - (no_games - invalid_games))
plt.bar(player_names, games_won)
plt.title("Closest First Vs. Farthest First")
plt.show()
plt.savefig("/figs/fig1")
print("Invalid Games: " + str(invalid_games))
