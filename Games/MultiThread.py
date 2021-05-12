from Players.Bots.BasicBots import *
from Structure.TransEuropa import TransEuropa
import matplotlib.pyplot as plt
from multiprocessing import Pool
import datetime
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
ESTIMATION_FILE = "est.txt"


class GameDriver:
	def run_games(self, no_games, players, map_filepath):
		games_won = [0] * len(players)
		turns = 0
		invalid_games = 0
		for i in range(0, no_games):
			if self.dl or (i + 1) in self.n_vals:
				print("----------Process:" + str(os.getpid()).ljust(6, ' ') + "| Game " + str(i + 1) + "----------")
			game = TransEuropa(players, map_filepath, self.dl, self.draw)
			game.play_game()
			if game.turn_count >= game.MAX_TURNS:
				invalid_games += 1
			turns += game.turn_count
			for j in range(0, len(players)):
				if players[j].has_won():
					games_won[j] += 1
				players[j].reset()
		player_names = []
		for player in players:
			player_names.append(player.name)
		score_dict = {}
		for i in range(len(player_names)):
			score_dict[player_names[i]] = games_won[i]
		score_dict["Draws"] = games_won[0] + games_won[1] - no_games
		if invalid_games:
			print("+++++++++")
			print("+INVALID+")
			print("+++++++++")
		return [score_dict, invalid_games, turns / self.games_per_process]

	def aggregate_results(self, res_to_agg):
		players = list(res_to_agg[0][0].keys())
		scores = {}
		for player in players:
			scores[player] = 0
		turns = 0
		inv_games = 0
		for res in res_to_agg:
			for i in range(0, len(players)):
				scores[players[i]] += res[0].get(players[i])
			inv_games += res[1]
			turns += res[2]
		if len(players) > 3:
			players.remove(players[len(players) - 1])
			scores.pop("Draws")
		else:
			draws = scores.get("Draws")
			for key in scores.keys():
				if key != "Draws":
					scores[key] -= draws
		return [players, scores, inv_games, turns / self.no_processes]

	def __init__(self, map_filepath: str, processes: int, games_per_process: int, debug_level: int, draw: int,
	             notification_vals: [int] = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]):
		self.map_filepath = map_filepath
		self.no_processes = processes
		self.games_per_process = games_per_process
		self.dl = debug_level
		self.draw = draw
		self.n_vals = notification_vals

	def simulate(self, players: [Player]):
		init_string = ""
		init_string += "Simulation Initiated:" + '\n'
		init_string += "Games To Simulate: " + str(self.games_per_process * self.no_processes) + '\n'
		if os.path.isfile(ESTIMATION_FILE):
			estimation_file = open(ESTIMATION_FILE)
			avg_game_time = float(estimation_file.read())
			estimation_file.close()
			if avg_game_time != 0:
				est_time = self.games_per_process * self.no_processes * avg_game_time
				init_string += "Average Game Time:" + str(avg_game_time) + '\n'
				init_string += "Estimated Time: " + str(datetime.timedelta(seconds=est_time))
			else:
				init_string += "Time Estimation Unavailable"
		else:
			estimation_file = open(ESTIMATION_FILE, "w")
			estimation_file.write("0")
			estimation_file.close()
			init_string += "Time Estimation Unavailable"
		print(init_string)
		start_time = datetime.datetime.now()
		params = [(self.games_per_process, players, self.map_filepath)] * self.no_processes
		results = []
		if self.no_processes > 1:
			if __name__ == 'Games.MultiThread':
				with Pool(self.no_processes) as p:
					results = p.starmap(self.run_games, params)
					p.close()
					p.join()
					results = self.aggregate_results(results)
		else:
			results = self.run_games(params[0][0], params[0][1], params[0][2])
		# printed /logfile output
		total_games = self.games_per_process * self.no_processes
		file_id = str((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
		title = params[0][1][0].name + " Vs. " + params[0][1][1].name + " (" + str(total_games) + " Games)"
		time_taken = datetime.datetime.now() - start_time
		avg_game_time = (time_taken / total_games).total_seconds()
		sb = "--------------------" + title + "--------------------\n"
		sb += "Player Wins:\n"
		for i in range(0, len(results[0])):
			sb += "    " + results[0][i] + ": " + str(results[1].get(results[0][i])) + " (" + str((results[1].get(results[0][i]) / total_games) * 100) + "%)" + '\n'
		sb += "Average Turns: " + str(results[3]) + '\n'
		sb += "Invalid Games: " + str(results[2]) + '\n'
		sb += "Total Time: " + str(time_taken) + '\n'
		sb += "    Average game time: " + str(avg_game_time) + " Seconds" + '\n'
		print(sb)
		log_file = open("out/logs/" + file_id + ".txt", 'w')
		log_file.write(sb)
		log_file.close()
		# Average Game time estimation
		estimation_file = open(ESTIMATION_FILE)
		prev_avg_time = float(estimation_file.read())
		estimation_file.close()
		estimation_file = open(ESTIMATION_FILE, 'w')
		if prev_avg_time == 0:
			estimation_file.write(str(avg_game_time))
		else:
			estimation_file.write(str((prev_avg_time + avg_game_time) / 2))
		estimation_file.close()
		# plot
		labels = []
		for i in range(0, len(results[0])):
			labels.append(str(results[1].get(results[0][i])) + " (" + str(round((results[1].get(results[0][i]) / total_games) * 100, 2)) + "%)")
		plt.pie(results[1].values(), labels=labels)
		title = ""
		for i in range(0, len(players)):
			if i != len(players) - 1:
				title += players[i].name + " Vs. "
			else:
				title += players[i].name

		title += "(" + str(total_games) + ")"
		plt.title(title)
		plt.legend(results[0], loc=2, bbox_to_anchor=(0.95, 0.6))
		plt.savefig("out/figs/" + file_id + ".png", bbox_inches='tight')
		plt.show()
