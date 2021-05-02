from Games.MultiThread import GameDriver
from Players.Bots.BasicBots import *

MAP_FILEPATH = "Structure/Maps/classic.txt"

game_driver = GameDriver(MAP_FILEPATH, 1, 64, 0, 0)

if __name__ == "__main__":
	game_driver.simulate([ClosestFirst("CF1"), ClosestFirst("CF2")])