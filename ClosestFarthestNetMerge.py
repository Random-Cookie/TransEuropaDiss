from Games.MultiThread import GameDriver
from Players.Bots.BasicBots import *
import warnings
warnings.filterwarnings("ignore")

MAP_FILEPATH = "Structure/Maps/classic.txt"

game_driver = GameDriver(MAP_FILEPATH, 10, 8192, 0, 0)

if __name__ == "__main__":
	game_driver.simulate(
		[ClosestFirst("Closest First"), FarthestFirst("Farthest First"), NetMergeFirst("Net Merge First", 1)])
	game_driver.simulate(
		[ClosestFirst("Closest First"), FarthestFirst("Farthest First"), NetMergeFirst("Net Merge First", 2)])
	game_driver.simulate(
		[ClosestFirst("Closest First"), FarthestFirst("Farthest First")])
	game_driver.simulate([
		ClosestFirst("Closest First"), NetMergeFirst("Net Merge First", 1)])
	game_driver.simulate([
		FarthestFirst("Farthest First"), NetMergeFirst("Net Merge First", 1)])
