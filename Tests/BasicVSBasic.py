import Structure.GameBoard as gb
from Players.Bots.BasicBot import BasicBot
from Graphics.DrawLib import BasicNetworkDrawer
import psychopy

comp1 = BasicBot("Comp1")
comp2 = BasicBot("Comp2")

test_board = gb.GameBoard([comp1, comp2], "Structure/Maps/classic.txt")

drawer = BasicNetworkDrawer(test_board.get_map(), test_board._cities)
win = psychopy.visual.Window(
	size=[1280, 720],
	units="pix",
	fullscr=False,
	color=[0.9, 0.9, 0.9]
)

moves = 0
MAX_MOVES = 100

for player in test_board.get_players():
	player.choose_start_pos(test_board)

game_won = False

while not game_won:
	for player in test_board.get_players():
		if not player.has_won() and not game_won:
			valid = False
			while not valid:
				co_ords = player.make_move(test_board)
				if test_board.is_valid_move(player, co_ords):
					player.add_node_to_network(test_board, co_ords)
					valid = True
		else:
			game_won = True
	drawer.draw_edges(win)
	drawer.draw_nodes(win)
	drawer.draw_cities(win)
	win.flip()
	input("Enter to cont...")
	moves += 1

print("OMFG IT ACTUALLY WORKED")
print("Moves: " + str(moves))
input("Press Enter to Exit...")
win.close()
quit()