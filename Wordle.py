import json
import numpy as np
import string
class Wordle():

	def __init__(self, lives, dict_path, set_word = None, ultra_instinct = False):
		self.lives = lives
		with open(dict_path, "r") as read_json:
			self.word_bank = np.array([i.strip().lower() for i in json.load(read_json)])
		
		self.word = set_word if set_word else np.random.choice(self.word_bank)
		self.encoded_word = self.encode_word(self.word)
		self.guesses = [[] for i in range(self.lives)]
		self.encoded_guesses = []
		self.turn = 0
		self.success = 0
		self.possible_letters = [w for w in string.ascii_lowercase]
		self.ultra_instinct = ultra_instinct

	def play_game(self):
		word = ""
		while self.turn < self.lives and not self.success:
			word, q = self.get_user_guess()
			if q:
				self.success = -1
				break
			formatted_guess, encoded_guess = self.format_guess_by_word(word)
			self.guesses[self.turn] = formatted_guess
			self.encoded_guesses.append(encoded_guess)
			self.success = 1 if (word == self.word) else 0
			self.turn += 1
		self.print_game_state()
		if self.success == 1:
			print(f"You win! The word is {self.word}!\n\n")
		elif self.success == 0:
			print(f"So close! The word is {self.word}!\n\n")
		else:
			print("Game quitted")

	def advance_state(self, word, verbose = True):

		formatted_guess, encoded_guess = self.format_guess_by_word(word)
		self.guesses[self.turn] = formatted_guess
		self.encoded_guesses.append(encoded_guess)
		self.success = 1 if (word == self.word) else 0
		self.turn += 1

		if verbose:
			self.print_game_state()

		if self.ultra_instinct:
			return encoded_guess, self.success, ((self.turn + 1) == self.lives)
		return encoded_guess, self.success
	
	def encode_word(self, word):
		encoded_word = {}
		for i, l in enumerate(word):
			if l not in encoded_word.keys():
				encoded_word[l] = [i]
			else:
				encoded_word[l].append(i)

		return encoded_word

	def format_guess_by_word(self, guess):
		checked_letters = set()
		word_guess = [g for g in self.word]
		formatted_guess = [None for i in range(len(guess))]
		encoded_guess = [None for i in range(len(guess))]

		checked_indicies = []

		for i, l in enumerate(guess):
			if l in word_guess:
				if i in self.encoded_word[l]:
					formatted_guess[i] = l.upper()
					encoded_guess[i] = [l, 3]
					word_guess[i] = "_"
					checked_indicies.append(i)
		
		for i, l in enumerate(guess):
			if i in checked_indicies:
				continue
				
			if (l in word_guess) and (l not in checked_letters):
				formatted_guess[i] = l + "*"
				encoded_guess[i] = [l, 2]
				checked_indicies.append(i)
				# word_guess[i] = "_"
				checked_letters.add(l)
		
		for i, l in enumerate(guess):
			if i in checked_indicies:
				continue

			formatted_guess[i] = l
			encoded_guess[i] = [l, 1]
			if l in self.possible_letters:
				self.possible_letters.remove(l)



		# for i, l in enumerate(guess):
		# 	stat = 0
		# 	if l in self.word:
		# 		stat += 1
		# 		if i in self.encoded_word[l]:
		# 			stat += 1
			
		# 	if stat == 0 and l in self.possible_letters:
		# 		self.possible_letters.remove(l)

		# 	if stat == 0 or (stat == 1 and l in checked_letters):
		# 		formatted_guess.append(l)
		# 		encoded_guess.append((l, 1))
		# 	elif stat == 1:
		# 		formatted_guess.append(l + "*")
		# 		encoded_guess.append((l, 2))
		# 	elif stat == 2:
		# 		formatted_guess.append(l.upper())
		# 		encoded_guess.append((l, 3))

		# 	checked_letters.add(l)
			
		return formatted_guess, encoded_guess
			
	def get_user_guess(self):
		w = ""

		while w not in self.word_bank and w != "quit":
			self.print_game_state()
			print("Please enter a 5 letter word: ")
			w = input().strip().lower()
			print(w)
		
		return w, w == "quit"

	def print_game_state(self):
		print("\n\n-----------------------")
		print(f"Turn {self.turn}")
		print(f"Possible Letters: {' '.join(self.possible_letters)}")
		print("-----------------------")
		for g in self.guesses:
			if len(g) != 0:
				print(" ".join(g))
			else:
				print("_ _ _ _ _")
			print()
		print("-----------------------\n\n")

if __name__ == "__main__":
	dict_path = "/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json"
	wordle = Wordle(6, dict_path)
	wordle.play_game()