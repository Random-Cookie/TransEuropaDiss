from Players.Player import Player
import networkx
from Structure.GameBoard import GameBoard


class BasicBot(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		self.target_cities = []
		self._current_path = []

	def choose_start_pos(self, game_board: GameBoard) -> str:
		start_city = self._cities[0]
		self.target_cities.remove(start_city)
		self.add_start_node(start_city)
		self._current_path = self.get_path_to_next_city(game_board)
		return start_city.get_id()

	def make_move(self, game_board: GameBoard) -> [str, str]:  # node to add to network should always be first
		if len(self._current_path) == 0:
			self._current_path = self.get_path_to_next_city(game_board)
			return self.make_move(game_board)
		else:
			next_node = self._current_path[0]
			self._current_path.remove(next_node)
			return next_node.get_id()[:2], next_node.get_id()[2:4]

	def set_cities(self, cities):
		self._cities = cities
		self.target_cities = cities

	def get_path_to_next_city(self, game_board: GameBoard):
		paths = networkx.single_source_dijkstra(game_board.get_map(), self.target_cities[0], weight='weight')
		self.target_cities.remove(self.target_cities[0])
		paths = self.collapse_paths(paths)
		possible_paths = []
		for path in paths:
			if path[0] in self._network:
				possible_paths.append(path)

		sorted_paths = sorted(possible_paths, key=lambda tup: tup[2])
		ret = sorted_paths[0][1]
		ret.reverse()
		return ret

	@staticmethod
	def collapse_paths(found_paths):
		distances = found_paths[0]
		paths = found_paths[1]
		collapsed = []
		for path in paths:
			collapsed.append((path, paths.get(path), distances.get(path)))
		return collapsed
