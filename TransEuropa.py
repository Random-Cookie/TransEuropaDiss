from Structure.GameBoard import GameBoard
from Graphics.DrawLib import BasicNetworkDrawer
import psychopy
import networkx


class TransEuropa:
	def __init__(self, players: [], map_filepath: str, debug_level: int, draw: bool = 0):
		self.__players = players
		self._map_filepath = map_filepath
		self.__board = GameBoard(self.__players, self._map_filepath)
		self.draw = draw
		if self.draw:
			self.__drawer = BasicNetworkDrawer(self.__board.get_map(), self.__board.get_cities())
			self.__win = psychopy.visual.Window(
				size=[1280, 720],
				units="pix",
				fullscr=False,
				color=[0.9, 0.9, 0.9]
			)
		self.turn_count = 0

	def reset_game(self):
		self.__board = GameBoard(self.__players, self._map_filepath)
		self.turn_count = 0
		for player in self.__players:
			player.reset()

	def play_game(self):
		# Players choose starting pos
		for player in self.__board.get_players():
			player.choose_start_pos(self.__board)
		game_won = False
		turns = 0
		while not game_won:
			turns += 1
			print("Turn " + str(turns) + ":")
			for player in self.__board.get_players():
				if not player.has_won() and not game_won:
					valid = False
					while not valid:
						co_ords = player.make_move(self.__board)
						if self.__board.is_valid_move(player, co_ords):
							player.add_node_to_network(self.__board, co_ords)
							valid = True
				else:
					game_won = True
				if self.draw == 2:
					self.draw_board()
		self.end_game(turns)

	def end_game(self, turns):
		for player in self.__players:
			if player.has_won():
				print(player.name + " Has Won!!")
		print("Winning Turn: " + str(turns))
		if self.draw:
			self.draw_board()

	def generate_player_scores(self) -> []:
		for player in self.__players:
			# protected access allowed in this case as this is driver code, it is protected to prevent access by other players
			unconnected_cities = player._cities not in player.get_network()
			for city in unconnected_cities:
				paths = networkx.single_source_dijkstra(self.__board, city, weight='weight')
				paths = self.collapse_paths(paths, player)


	@staticmethod
	def collapse_paths(found_paths, player):
		distances = found_paths[0]
		paths = found_paths[1]
		collapsed = []
		for path in paths:
			if path[len(path) - 1] in player.get_network():
				collapsed.append((path, paths.get(path), distances.get(path)))
		return collapsed

	def draw_board(self):
		self.__drawer.draw_edges(self.__win)
		self.__drawer.draw_nodes(self.__win)
		self.__drawer.draw_cities(self.__win)
		self.__win.flip()
