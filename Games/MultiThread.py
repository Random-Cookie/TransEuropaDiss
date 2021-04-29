from Players.Bots.BasicBots import *
from TransEuropa import TransEuropa
import matplotlib.pyplot as plt
from multiprocessing import Pool
import datetime


def run_games(no_games, players, map_filepath):
	games_won = [0] * len(players)
	invalid_games = 0
	for i in range(0, no_games):
		print("----------Game " + str(i) + "----------")
		game = TransEuropa(players, map_filepath, DEBUG_LEVEL, 0)
		game.play_game()
		if game.turn_count >= game.MAX_TURNS:
			invalid_games += 1
		for j in range(0, len(players)):
			if players[j].has_won():
				games_won[j] += 1
			players[j].reset()
	player_names = []
	for player in players:
		player_names.append(player.name)
	player_names.append("Draws")
	games_won.append((games_won[0] + games_won[1]) - (no_games))
	if invalid_games:
		print("+++++++++")
		print("+INVALID+")
		print("+++++++++")
	return [player_names, games_won, invalid_games]


def aggregate_results(res_to_agg):
	players = res_to_agg[0][0]
	scores = [0] * len(players)
	inv_games = 0
	for res in res_to_agg:
		for i in range(0, len(players)):
			scores[i] += res[1][i]
		inv_games += res[2]
	if len(players) > 2:
		players.remove(players[len(players) - 1])
		scores.remove(scores[len(scores) - 1])
	else:
		draws = scores[len(scores) - 1]
		for i in range(0, len(scores) - 1):
			scores[i] -= draws
	return [players, scores, inv_games]


NO_OF_PROCESSES = 8
GAMES_PER_PROCESS = 32
DEBUG_LEVEL = 1
DRAW = 0

start_time = datetime.datetime.now()

params = [(GAMES_PER_PROCESS, [ClosestFirst("Closest First"), FarthestFirst("Farthest First"), NetMergeFirst("NetMerge First", 5)], "Structure/Maps/classic.txt")] * NO_OF_PROCESSES
results = []
if __name__ == '__main__':
	with Pool(NO_OF_PROCESSES) as p:
		results = p.starmap(run_games, params)
		p.close()
		p.join()
	results = aggregate_results(results)
	total_games = GAMES_PER_PROCESS * NO_OF_PROCESSES
	print("-------------------------------------------------------")
	print("Player Wins:")
	for i in range(0, len(results[0])):
		print("    " + results[0][i] + ": " + str(results[1][i]) + "  (" + str((results[1][i] / total_games) * 100) + "%)")
	print("Invalid Games: " + str(results[2]))
	time_taken = datetime.datetime.now() - start_time
	print("Ran " + str(total_games) + " Games in " + str(time_taken))
	print("    Average game time: " + str((time_taken / total_games).total_seconds()) + " Seconds")
	# plot
	labels = []
	for i in range(0, len(results)):
		labels.append(str(results[1][i]) + " (" + str(round((results[1][i] / total_games) * 100, 2)) + "%)")
	plt.pie(results[1], labels=labels)
	plt.title(params[0][1][0].name + " Vs. " + params[0][1][1].name + " (" + str(total_games) + " Games)")
	plt.legend(results[0], loc='center left', bbox_to_anchor=(0.98, 0.1))
	plt.savefig("figs/fig" + str((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()) + ".png")
	plt.show()
