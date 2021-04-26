import Structure.GameBoard as gb
from Players.Bots.BasicBot import BasicBot

test_player = BasicBot("Comp1")

test_board = gb.GameBoard([test_player], "Structure/Maps/classic.txt")

moves = 0
MAX_MOVES = 100

test_player.choose_start_pos(test_board)

game_won = False

while not game_won:
	moves += 1
	for player in test_board.get_players():
		chosen_node = player.make_move(test_board)
		test_player.add_node_to_network(test_board, chosen_node)

		# print("----------")
		# player.print_nodes_in_network()
		# print("----------")
		# player.print_cities_in_network(test_board)
		# print("----------")
		# player.print_edges_in_network()

		if player.has_won():
			game_won = True

print("OMFG IT ACTUALLY WORKED")
print("Moves: " + str(moves))
