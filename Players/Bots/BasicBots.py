from Players.Player import Player
import networkx
from Structure.GameBoard import GameBoard
import copy


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
		self.target_cities = copy.copy(cities)

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
		self.target_cities = copy.copy(cities)

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
		self.add_start_node(start_city)
		return start_city.get_id()

	def make_move(self, game_board: GameBoard) -> [str, str]:  # node to add to network should always be first
		self._current_path = self.get_next_path(game_board)
		if self._current_path != "w":
			# while self._current_path[1] in self._network.nodes:
			# 	self._current_path.remove(self._current_path[0])
			node_in_network_id = self._current_path[0].get_id()
			next_node_id = self._current_path[1].get_id()
			self._current_path.remove(self._current_path[0])
			return [next_node_id, node_in_network_id]
		else:
			return "w"

	def set_cities(self, cities):
		Player.set_cities(self, cities)
		# make target cities a shallow copy of cities to allow for removal of objects without removing from cities
		self._target_cities = copy.copy(cities)

	def get_next_path(self, game_board: GameBoard):
		if self.network_merge(game_board):
			self._sort_cities(game_board)
		if not self.has_won():
			paths = networkx.single_source_dijkstra(game_board.get_map(), self._target_cities[0], weight='weight')
			paths = self.collapse_paths(paths)
			possible_paths = []
			for path in paths:
				if (path[1][len(path[1]) - 1] in self._network.nodes) and path[2] != 0:
					possible_paths.append(path)
			# path filter to remove paths with many nodes in network
			i = 0
			while i < len(possible_paths):
				inter = len(set(possible_paths[i][1]) & set(self._network.nodes))
				if inter > 1 and len(possible_paths) > 1:
					possible_paths.remove(possible_paths[i])
					i -= 1
				i += 1
			sorted_paths = sorted(possible_paths, key=lambda tup: tup[2])
			if len(sorted_paths) <= 0:
				return self.get_next_path(game_board)
			optimal_path = sorted_paths[0]
			optimal_path[1].reverse()
			return optimal_path[1]
		else:
			return "w"

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

	def network_merge(self, game_board: GameBoard) -> bool:
		ret = False
		for player in game_board.get_players():
			for node in player.get_network().nodes:
				if node in self._network:
					self._network = networkx.compose(self._network, player.get_network())
					ret = True
					break
		return ret

	def _sort_cities(self, game_board: GameBoard):
		lengths = {}
		start_city = self._target_cities[0]
		for i in range(0, len(self._target_cities)):
			lengths[self._target_cities[i]] = networkx.shortest_path_length(game_board.get_map(), start_city, self._target_cities[i])
		lengths = dict(sorted(lengths.items(), key=lambda item: item[1]))
		self._target_cities = list(lengths.keys())


class FarthestFirst(ClosestFirst):
	def _sort_cities(self, game_board: GameBoard):
		lengths = {}
		start_city = self._target_cities[0]
		for i in range(0, len(self._target_cities)):
			lengths[self._target_cities[i]] = networkx.shortest_path_length(game_board.get_map(), start_city, self._target_cities[i])
		lengths = dict(reversed(sorted(lengths.items(), key=lambda item: item[1])))
		self._target_cities = list(lengths.keys())


class NetMergeFirst(ClosestFirst):
	def __init__(self, name, players_to_merge):
		ClosestFirst.__init__(self, name)
		self._players_to_connect = players_to_merge
		self._connected_players = 0

	def get_next_path(self, game_board: GameBoard):
		if self.network_merge(game_board):
			self._sort_cities(game_board)
		if self._connected_players < self._players_to_connect:
			unconnected_players = []
			self._connected_players = 0
			for player in game_board.get_players():
				if not networkx.is_isomorphic(self._network, player.get_network()):
					unconnected_players.append(player)
				else:
					self._connected_players += 1
			shortest_path = [None, None, 0]
			for player in unconnected_players:
				player_nodes = player.get_network().nodes
				for node in player_nodes:
					player_paths = networkx.single_source_dijkstra(game_board.get_map(), node, weight='weight')
					player_paths = self.collapse_paths(player_paths)
					for path in player_paths:
						if path[1][len(path[1]) - 1] in self._network:
							if path[2] < shortest_path[2]:
								shortest_path = path
			if shortest_path[2] > 0:
				return shortest_path
		return ClosestFirst.get_next_path(self, game_board)


class Closestx(ClosestFirst):
	def __init__(self, name: str, x: int):
		ClosestFirst.__init__(self, name)
		self.x = x

	def choose_start_pos(self, game_board: GameBoard) -> str:
		group_weights = []
		sublists = self.generate_sublists()
		rem = 0
		while rem < len(sublists):
			if len(sublists[rem]) != self.x:
				sublists.remove(sublists[rem])
				rem -= 1
			rem += 1
		for i in sublists:
			path_lengths = []
			for j in range(0, len(i)):
				for k in range(0, len(i) - 1):
					path_lengths.append(networkx.shortest_path_length(game_board.get_map(), i[j], i[k]))
			while len(path_lengths) > self.x:
				path_lengths.remove(max(path_lengths))
			group_weights.append([i, sum(path_lengths)])
		closest_group = group_weights[0]
		dist = group_weights[0][1]
		for i in range(0, len(group_weights)):
			if group_weights[i][1] < dist:
				closest_group = group_weights[i]
				dist = group_weights[i][1]
		start_city = closest_group[0][0]
		self.add_start_node(start_city)
		return start_city.get_id()

	def generate_sublists(self):
		ret = [[]]
		for i in range(len(self._cities) + 1):
			for j in range(i + 1, len(self._cities) + 1):
				sub = self._cities[i:j]
				ret.append(sub)
		return ret
