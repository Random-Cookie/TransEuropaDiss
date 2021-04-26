import Structure.GameBoard as gb
from Players.HumanPlayer import HumanPlayer

test_player = HumanPlayer("Joe")

test_board = gb.GameBoard([test_player], "Structure/Maps/classic.txt")

moves = 0
MAX_MOVES = 100

chosen_node = test_player.choose_start_pos(test_board)
node = test_board.get_nodes().get(chosen_node)
test_player.add_start_node(node)

print("Score: " + str(test_player.generate_score(test_board)))

while moves < MAX_MOVES:
	moves += 1
	for player in test_board.get_players():
		chosen_node = player.make_move(test_board)
		test_player.add_node_to_network(test_board, chosen_node)
		print("Score: " + str(test_player.generate_score(test_board)))