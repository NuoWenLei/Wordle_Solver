from Sedordle_Website_Game import Sedordle_Website_Game
from general_solver import General_Solver
import numpy as np, json, string

if __name__ == "__main__":
	dict_path = "/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json"
	game = Sedordle_Website_Game(ultra_instinct=True, daily = True)
	trisha = General_Solver(dict_path, game, num_game_boards=16)
	trisha.live_play_ultra()

