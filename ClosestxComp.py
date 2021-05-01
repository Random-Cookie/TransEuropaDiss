from Games.MultiThread import GameDriver
from Players.Bots.BasicBots import *

MAP_FILEPATH = "Structure/Maps/classic.txt"

game_driver = GameDriver(MAP_FILEPATH, 8, 8192, 0, 0)

if __name__ == "__main__":
	game_driver.simulate([Closestx("Closest Pair", 2), Closestx("Closest 3", 3), Closestx("Closest 4", 4)])
	game_driver.simulate([Closestx("Closest Pair", 2), Closestx("Closest 3", 3)])
	game_driver.simulate([Closestx("Closest 2", 2), Closestx("Closest 4", 4)])
	game_driver.simulate([Closestx("Closest 3", 3), Closestx("Closest 4", 4)])