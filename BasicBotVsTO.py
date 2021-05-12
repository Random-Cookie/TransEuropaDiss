from Games.MultiThread import GameDriver
from Players.Bots.BasicBots import *
import warnings
warnings.filterwarnings("ignore")

MAP_FILEPATH = "Structure/Maps/classic.txt"

game_driver = GameDriver(MAP_FILEPATH, 10, 8192, 0, 0)

if __name__ == "__main__":
	game_driver.simulate([BasicBot("Basic Bot"), TrackOptimised("Track Optimised")])
	game_driver.simulate([TrackOptimised("Track Optimised"), ClosestFirst("Closest First")])