import networkx as nx


class GameBoard:
	def __add_node(self, cities: dict, node_id: str):
		pass
		# TODO: add node to graph

	def __add_edge(self, double_tracks: dict, node_id: str):
		pass
		# TODO: add edge to graph

	@staticmethod
	def map_cities(city_list: str) -> dict:
		pass
		# TODO: map cities from file

	@staticmethod
	def map_double_tracks(track_list: []) -> dict:
		pass
		# TODO: map double tracks from file

	def __generate_map(self, filepath: str):
		pass
		# TODO: generate the map

	def __set_player_cities(self):
		pass
		# TODO: give each player some cities

	def __init__(self, players: list, map_filepath: str):
		self._players = players
		self._nodes = {}
		self._cities = {}
		self._edges = {}
		self.__map = nx.Graph()
		self.__generate_map(map_filepath)
		self.__set_player_cities()

	def get_map(self):
		return self.__map

	def get_cities(self):
		return self._cities

	def get_nodes(self):
		return self._nodes

	def get_players(self):
		return self._players

	def get_edges(self):
		return self._edges

	def find_distance(self):
		pass
		# TODO: implement path find
