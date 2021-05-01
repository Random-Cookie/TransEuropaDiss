from multiprocessing.dummy import freeze_support

from Players.Bots.BasicBots import *
from Structure.TransEuropa import TransEuropa
import matplotlib.pyplot as plt
from multiprocessing import Pool
import datetime
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class GameDriver:
	def run_games(self, no_games, players, map_filepath):
		games_won = [0] * len(players)
		invalid_games = 0
		for i in range(0, no_games):
			if self.dl or i in self.n_vals:
				print("----------Game " + str(i) + "----------")
			game = TransEuropa(players, map_filepath, self.dl, 0)
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
		games_won.append((games_won[0] + games_won[1]) - no_games)
		if invalid_games:
			print("+++++++++")
			print("+INVALID+")
			print("+++++++++")
		return [player_names, games_won, invalid_games]

	@staticmethod
	def aggregate_results(res_to_agg):
		players = res_to_agg[0][0]
		scores = [0] * len(players)
		inv_games = 0
		for res in res_to_agg:
			for i in range(0, len(players)):
				scores[i] += res[1][i]
			inv_games += res[2]
		if len(players) > 3:
			players.remove(players[len(players) - 1])
			scores.remove(scores[len(scores) - 1])
		else:
			draws = scores[len(scores) - 1]
			for i in range(0, len(scores) - 1):
				scores[i] -= draws
		return [players, scores, inv_games]
	
	def __init__(self, map_filepath: str, processes: int, games_per_process: int, debug_level: int, draw: int, notification_vals: [int] = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]):
		self.map_filepath = map_filepath
		self.no_processes = processes
		self.games_per_process = games_per_process
		self.dl = debug_level
		self.draw = draw
		self.n_vals = notification_vals
	
	def simulate(self, players: [Player]):
		start_time = datetime.datetime.now()
		params = [(self.games_per_process, players, self.map_filepath)] * self.no_processes
		results = []
		if __name__ == 'Games.MultiThread':
			freeze_support()
			with Pool(self.no_processes) as p:
				results = p.starmap(self.run_games, params)
				p.close()
				p.join()
			results = self.aggregate_results(results)
			total_games = self.games_per_process * self.no_processes
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
			for i in range(0, len(results[0])):
				labels.append(str(results[1][i]) + " (" + str(round((results[1][i] / total_games) * 100, 2)) + "%)")
			plt.pie(results[1], labels=labels)
			title = ""
			for i in range(0, len(players)):
				if players[i].name != "draw":
					title += players[i].name + " Vs. "
				if i == len(players) - 1:
					title.rstrip(" Vs. ")
			title += "(" + str(total_games) + ")"
			plt.title(params[0][1][0].name + " Vs. " + params[0][1][1].name + " (" + str(total_games) + " Games)")
			plt.legend(results[0], loc='center left', bbox_to_anchor=(0.98, 0.1))
			plt.savefig("out/fig" + str((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()) + ".png")
			plt.show()
