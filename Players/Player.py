import networkx as nx
from networkx import Graph
from abc import abstractmethod

from Graphics.DrawLib import NetworkToPoints
from Structure.GameBoard import GameBoard
from Structure.Nodes import *


class Player:
	def __init__(self, name):
		self.name = name
		self._network = Graph()
		self._cities = {}
		self.__score = 0

	def set_cities(self, cities):
		""" Set cities for a player, any overide must run Player.set_cities()

		:param cities: cities for the player
		:return: none
		"""
		self._cities = cities

	def get_network(self):
		return self._network

	def get_score(self):
		return self.__score

	def add_score(self, score):
		self.__score += score

	def reset(self):
		self._network = Graph()
		self._cities = {}
		self.__score = 0

	def print_nodes_in_network(self):
		points = NetworkToPoints.get_node_points(self._network)
		for point in points:
			print("Node: " + str(point[0]).rjust(2, "0") + "," + str(point[1]).rjust(2, "0"))

	def print_cities_in_network(self, game_board: GameBoard):
		groups = NetworkToPoints.get_city_points(self._network)
		for group in groups:
			if group:
				for point in group:
					city = game_board.get_cities().get(str(point[0]).rjust(2, "0") + str(point[1]).rjust(2, "0"))
					print(city.get_name() + ": " + str(point[0]).rjust(2, "0") + "," + str(point[1]).rjust(2, "0"))

	def print_edges_in_network(self):
		lines = NetworkToPoints.get_edge_lines(self._network)
		for line in lines:
			print("Edge: " + str(line[0][0]).rjust(2, "0") + "," + str(line[0][1]).rjust(2, "0")
			      + str(line[1][0]).rjust(2, "0") + "," + str(line[1][1]).rjust(2, "0"))

	def add_start_node(self, node: Node):
		self._network.add_node(node)

	def add_node_to_network(self, game_board: GameBoard, chosen_node: [str, str]):
		self._network.add_node(game_board.get_nodes().get(chosen_node[0]))
		edge = game_board.get_edges().get(chosen_node[0] + chosen_node[1])
		if edge is None:
			edge = game_board.get_edges().get(chosen_node[1] + chosen_node[0])
		try:
			game_board.get_map()[edge[0]][edge[1]]['weight'] = 0
			self._network.add_edge(edge[0], edge[1], weight=0)
		except TypeError as err:
			print("error: {0}".format(err))

	@abstractmethod
	def choose_start_pos(self, game_board: GameBoard) -> str:
		print(self.name + " chose their starting position")
		return "0000"

	@abstractmethod
	def make_move(self, game_board: GameBoard) -> [str]:
		print(self.name + " took a turn")
		return ["0000", "0000"]

	def has_won(self):
		"""Has won function, any override must return Player.has_won(self)

		:return: if player has won
		"""
		for city in self._cities:
			if city not in self._network.nodes:
				return False
		return True

	def _score_path(self, a: Node, b: Node, game_board: GameBoard) -> int:
		return nx.shortest_path_length(game_board.get_map(), a, b)
