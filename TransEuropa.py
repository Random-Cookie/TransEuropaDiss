from Structure.GameBoard import GameBoard


class TransEuropa:
	def __init__(self, players: [], map_filepath: str):
		self.__board = GameBoard(players, map_filepath)
		self.__players = players
		self._map_filepath = map_filepath

	def reset_game(self):
		self.__board = GameBoard(self.__players, self._map_filepath)

	def play_game(self):
		# Players choose starting pos
		for player in self.__board.get_players():
			player.choose_start_pos()
		finished = False
		while not finished:
			# Each player makes a move
			for player in self.__board.get_players():
				player.make_move()
				# Check if player has won
				if player.has_won():
					finished = True
					break
	# TODO: Implement game play

	def generate_player_scores(self) -> []:
		r = []
		for player in self.__board.get_players():
			if not player.has_won():
				r.append(player.generate_score())
		return r
