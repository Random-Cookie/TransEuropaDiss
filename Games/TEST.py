from TransEuropa import TransEuropa
from Players.Bots.TrackOptimised import TrackOptimised

players = [TrackOptimised("Comp 1"), TrackOptimised("Comp 2")]
map_filepath = "Structure/Maps/classic.txt"

game = TransEuropa(players, map_filepath, 0)

game.play_game()
