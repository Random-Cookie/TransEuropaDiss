from Games.MultiThread import GameDriver
from Players.Bots.BasicBots import *

MAP_FILEPATH = "Structure/Maps/classic.txt"

game_driver = GameDriver(MAP_FILEPATH, 4, 32, 0, 0)

if __name__ == "__main__":
	game_driver.simulate([ClosestFirst("Closest First"), ClosestX("Closest 2", 2), ClosestX("Closest 3", 2)])

