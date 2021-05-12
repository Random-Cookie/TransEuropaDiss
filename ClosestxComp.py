from Games.MultiThread import GameDriver
from Players.Bots.BasicBots import *

MAP_FILEPATH = "Structure/Maps/classic.txt"

game_driver = GameDriver(MAP_FILEPATH, 10, 8192, 0, 0)

if __name__ == "__main__":
	game_driver.simulate([ClosestX("Closest 2", 2), ClosestX("Closest 3", 3), ClosestX("Closest 4", 4)])
	game_driver.simulate([ClosestX("Closest 2", 2), ClosestX("Closest 3", 3)])
	game_driver.simulate([ClosestX("Closest 2", 2), ClosestX("Closest 4", 4)])
	game_driver.simulate([ClosestX("Closest 3", 3), ClosestX("Closest 4", 4)])
	print("--------------------------------------------------")
	print("COMPLETED")
	print("--------------------------------------------------")