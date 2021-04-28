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
		if len(self._current_path) == 0 and not self.has_won():
			self._current_path = self.get_path_to_next_city(game_board)
			return self.make_move(game_board)
		elif len(self._current_path) == 1 and not self.has_won():
			self._current_path.remove(self._current_path[0])
			return self.make_move(game_board)
		else:
			node_in_network_id = self._current_path[0].get_id()
			next_node_id = self._current_path[1].get_id()
			self._current_path.remove(self._current_path[0])
			return [next_node_id, node_in_network_id]

	def set_cities(self, cities):
		self._cities = cities
		# make target cities a shallow copy of cities to allow for removal of objects without removing from cities
		self.target_cities = list(cities)

	def get_path_to_next_city(self, game_board: GameBoard):
		paths = networkx.single_source_dijkstra(game_board.get_map(), self.target_cities[0], weight='weight')
		self.target_cities.remove(self.target_cities[0])
		paths = self.collapse_paths(paths)
		possible_paths = []
		for path in paths:
			if path[1][len(path[1]) - 1] in self._network:
				possible_paths.append(path)
		sorted_paths = sorted(possible_paths, key=lambda tup: tup[2])
		sorted_paths[0][1].reverse()
		return sorted_paths[0][1]

	@staticmethod
	def collapse_paths(found_paths):
		distances = found_paths[0]
		paths = found_paths[1]
		collapsed = []
		for path in paths:
			collapsed.append((path, paths.get(path), distances.get(path)))
		return collapsed


class TrackOptimised(Player):
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
		self._current_path = self.get_path_to_next_city(game_board)
		node_in_network_id = self._current_path[0].get_id()
		next_node_id = self._current_path[1].get_id()
		self._current_path.remove(self._current_path[0])
		return [next_node_id, node_in_network_id]

	def set_cities(self, cities):
		Player.set_cities(self, cities)
		# make target cities a shallow copy of cities to allow for removal of objects without removing from cities
		self.target_cities = list(cities)

	def get_path_to_next_city(self, game_board: GameBoard):
		self.network_merge(game_board)
		paths = networkx.single_source_dijkstra(game_board.get_map(), self.target_cities[0], weight='weight')
		paths = self.collapse_paths(paths)
		possible_paths = []
		for path in paths:
			if path[1][len(path[1]) - 1] in self._network:
				possible_paths.append(path)
		sorted_paths = sorted(possible_paths, key=lambda tup: tup[2])
		optimal_path = sorted_paths[0]
		if optimal_path[2] == 0:
			optimal_path = sorted_paths[1]
		optimal_path[1].reverse()
		return optimal_path[1]

	@staticmethod
	def collapse_paths(found_paths):
		distances = found_paths[0]
		paths = found_paths[1]
		collapsed = []
		for path in paths:
			collapsed.append((path, paths.get(path), distances.get(path)))
		return collapsed

	def has_won(self):
		for city in self.target_cities:
			if city in self._network.nodes:
				self.target_cities.remove(city)
		return Player.has_won(self)

	def network_merge(self, game_board: GameBoard):
		for player in game_board.get_players():
			for node in player.get_network().nodes:
				if node in self._network:
					self._network = networkx.compose(self._network, player.get_network())


class ClosestFirst(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		self._target_cities = []
		self._current_path = []

	def choose_start_pos(self, game_board: GameBoard) -> str:
		start_city = self._cities[0]
		self._target_cities.remove(start_city)
		self.add_start_node(start_city)
		self._current_path = self.get_path_to_next_city(game_board)
		return start_city.get_id()

	def make_move(self, game_board: GameBoard) -> [str, str]:  # node to add to network should always be first
		self._current_path = self.get_path_to_next_city(game_board)
		node_in_network_id = self._current_path[0].get_id()
		next_node_id = self._current_path[1].get_id()
		self._current_path.remove(self._current_path[0])
		return [next_node_id, node_in_network_id]

	def set_cities(self, cities):
		Player.set_cities(self, cities)
		# make target cities a shallow copy of cities to allow for removal of objects without removing from cities
		self._target_cities = list(cities)

	def get_path_to_next_city(self, game_board: GameBoard):
		self.network_merge(game_board)
		self._sort_cities(game_board)
		paths = networkx.single_source_dijkstra(game_board.get_map(), self._target_cities[0], weight='weight')
		paths = self.collapse_paths(paths)
		possible_paths = []
		for path in paths:
			if path[1][len(path[1]) - 1] in self._network:
				possible_paths.append(path)
		sorted_paths = sorted(possible_paths, key=lambda tup: tup[2])
		optimal_path = sorted_paths[0]
		if optimal_path[2] == 0:
			optimal_path = sorted_paths[1]
		optimal_path[1].reverse()
		return optimal_path[1]

	@staticmethod
	def collapse_paths(found_paths):
		distances = found_paths[0]
		paths = found_paths[1]
		collapsed = []
		for path in paths:
			collapsed.append((path, paths.get(path), distances.get(path)))
		return collapsed

	def has_won(self):
		for city in self._target_cities:
			if city in self._network.nodes:
				self._target_cities.remove(city)
		return Player.has_won(self)

	def network_merge(self, game_board: GameBoard):
		for player in game_board.get_players():
			for node in player.get_network().nodes:
				if node in self._network:
					self._network = networkx.compose(self._network, player.get_network())

	def _sort_cities(self, game_board: GameBoard):
		lengths = {}
		start_city = self._target_cities[0]
		for i in range(0, len(self._target_cities)):
			lengths[self._target_cities[i]] = networkx.shortest_path_length(game_board.get_map(), start_city, self._target_cities[i])
		lengths = dict(sorted(lengths.items(), key=lambda item: item[1]))
		self._target_cities = list(lengths.keys())


class FarthestFirst(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		self._target_cities = []
		self._current_path = []

	def choose_start_pos(self, game_board: GameBoard) -> str:
		start_city = self._cities[0]
		self._target_cities.remove(start_city)
		self.add_start_node(start_city)
		self._current_path = self.get_path_to_next_city(game_board)
		return start_city.get_id()

	def make_move(self, game_board: GameBoard) -> [str, str]:  # node to add to network should always be first
		self._current_path = self.get_path_to_next_city(game_board)
		node_in_network_id = self._current_path[0].get_id()
		next_node_id = self._current_path[1].get_id()
		self._current_path.remove(self._current_path[0])
		return [next_node_id, node_in_network_id]

	def set_cities(self, cities):
		Player.set_cities(self, cities)
		# make target cities a shallow copy of cities to allow for removal of objects without removing from cities
		self._target_cities = list(cities)

	def get_path_to_next_city(self, game_board: GameBoard):
		self.network_merge(game_board)
		self._sort_cities(game_board)
		paths = networkx.single_source_dijkstra(game_board.get_map(), self._target_cities[0], weight='weight')
		paths = self.collapse_paths(paths)
		possible_paths = []
		for path in paths:
			if path[1][len(path[1]) - 1] in self._network:
				possible_paths.append(path)
		sorted_paths = sorted(possible_paths, key=lambda tup: tup[2])
		optimal_path = sorted_paths[0]
		if optimal_path[2] == 0:
			optimal_path = sorted_paths[1]
		optimal_path[1].reverse()
		return optimal_path[1]

	@staticmethod
	def collapse_paths(found_paths):
		distances = found_paths[0]
		paths = found_paths[1]
		collapsed = []
		for path in paths:
			collapsed.append((path, paths.get(path), distances.get(path)))
		return collapsed

	def has_won(self):
		for city in self._target_cities:
			if city in self._network.nodes:
				self._target_cities.remove(city)
		return Player.has_won(self)

	def network_merge(self, game_board: GameBoard):
		for player in game_board.get_players():
			for node in player.get_network().nodes:
				if node in self._network:
					self._network = networkx.compose(self._network, player.get_network())

	def _sort_cities(self, game_board: GameBoard):
		lengths = {}
		start_city = self._target_cities[0]
		for i in range(0, len(self._target_cities)):
			lengths[self._target_cities[i]] = networkx.shortest_path_length(game_board.get_map(), start_city, self._target_cities[i])
		lengths = dict(reversed(sorted(lengths.items(), key=lambda item: item[1])))
		self._target_cities = list(lengths.keys())

