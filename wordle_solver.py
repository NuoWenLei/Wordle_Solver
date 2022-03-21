from Wordle import Wordle
from Wordle_Website_Game import Wordle_Website_Game
from Wordle_Archive_Game import Wordle_Archive_Game
import numpy as np, json, string

class Wordle_Reinforcement_Learning():
	def __init__(self, dict_path, manual = False, debug = False, set_word = None, live_play = False, ultra_instinct = False, archive = False, archive_num = None, end_with_close = False):

		# Select Wordle game mode:
		# - Local Wordle
		# - Archive Wordle
		# - Official Wordle
		if (not live_play) and (not archive):
			if end_with_close:
				raise Exception("Cannot close local game without driver")
			self.wordle_game = Wordle(6, dict_path, set_word = set_word, ultra_instinct = ultra_instinct)
		if live_play:
			self.wordle_game = Wordle_Website_Game(ultra_instinct = ultra_instinct)
		if archive:
			if not archive_num:
				raise Exception("No Archive Number Specified for Archive Mode")
			print(archive_num)
			self.wordle_game = Wordle_Archive_Game(archive_num, ultra_instinct = ultra_instinct)

		self.debug = debug
		self.encoded_guesses = []

		# Alphabet Encoding Dictionary
		self.letter_dict = dict((a, i) for i, a in enumerate(string.ascii_lowercase))

		# Load Vocabulary
		self.vocab = self.get_initial_vocab(dict_path)
		self.local_guesses = []
		self.manual = manual

		# For Optimized Performance
		self.ultra_instinct = ultra_instinct
		self.end_with_close = end_with_close

		if manual and debug:
			raise Exception("Cannot do manual encoded word inputs during debug mode")

	def update_guesses(self, guess_string):
		"""
		Converts manually entered string-encoded guess into officially encoded guess
		Input Example:
		m0 a* r* t_ s0

		Output Example:
		[
			['m', 1],
			['a', 2],
			['r', 2],
			['t', 3].
			['s', 1]
		]
		"""
		g = guess_string.strip().split(" ")

		enc_guess = []
		for l in g:
			if l[1] == "_":
				enc_guess.append([l[0].lower(), 3])
			
			elif l[1] == "*":
				enc_guess.append([l[0].lower(), 2])

			else:
				enc_guess.append([l[0].lower(), 1])
		
		self.encoded_guesses.append(enc_guess)

	def live_play(self):
		"""
		Trish will play Wordle Game live, reading and writing words on its own.
		This mode does not support ultra instinct or manual entering, but does support debug mode.

		Modes:
		x - ultra_instinct
		x - manual
		o - debug

		"""
		if self.ultra_instinct:
			raise Exception("Ultra Instinct mode not compatible with live_play(). Use live_play_ultra() instead!!!")
		done = False
		while not done:

			if self.debug:
				inp = input("Continue")

			state = self.get_state(self.encoded_guesses)
			print(state)
			vocab = Wordle_Reinforcement_Learning.vocab_filter_total(state, self.vocab)
			print(vocab.shape)
			# if inp == "vocabs":
			# 	print([Wordle_Reinforcement_Learning.to_word(w) for w in vocab])
			vocab_dist = Wordle_Reinforcement_Learning.get_vocab_distribution(vocab)
			info_list = Wordle_Reinforcement_Learning.word_information(vocab, vocab_dist, state)
			new_guess = max(info_list, key = lambda x: x[1])
			self.local_guesses.append(new_guess)
			max_info_guesses = sorted(info_list, key = lambda x: x[1], reverse = True)
			print([f"{Wordle_Reinforcement_Learning.to_word(w[0])}: {w[1]:.2f}" for w in max_info_guesses[0:10]])
			new_word_guess = Wordle_Reinforcement_Learning.to_word(new_guess[0])
			print(new_word_guess)

			new_enc_guess, done = self.wordle_game.advance_state(new_word_guess)

			self.encoded_guesses.append(new_enc_guess)

		print("DONE")

	def live_play_ultra(self):
		"""
		Trish will play Wordle Game live in ultra instinct mode,
		with optimized gameplay and automatic reading and writing.
		Variable ultra_instinct must be True to allow this mode.

		Modes:
		o - ultra_instinct
		x - manual
		o - debug

		"""
		if not self.ultra_instinct:
			raise Exception("Used Ultra Instinct mode but ultra_instinct is not turned on!!!")
		final_turn = False
		done = False
		while (not final_turn) and (not done):

			if self.debug:
				inp = input("Continue")

			state = self.get_state(self.encoded_guesses)
			print(state)
			vocab = Wordle_Reinforcement_Learning.vocab_filter_total(state, self.vocab)
			# if inp == "vocabs":
			# 	print([Wordle_Reinforcement_Learning.to_word(w) for w in vocab])

			zero_out_state = Wordle_Reinforcement_Learning.get_zero_out_state(state)
			vocab_dist = Wordle_Reinforcement_Learning.get_vocab_distribution(vocab)
			new_vocab_dist = vocab_dist * zero_out_state
			print(new_vocab_dist)
			print(vocab.shape)
			info_list = Wordle_Reinforcement_Learning.word_information(self.vocab, new_vocab_dist, state)
			max_info_guesses = sorted(info_list, key = lambda x: x[1], reverse = True)
			print([f"{Wordle_Reinforcement_Learning.to_word(w[0])}: {w[1]:.2f}" for w in max_info_guesses[0:10]])
			new_guess = max(info_list, key = lambda x: x[1])
			self.local_guesses.append(new_guess)
			new_word_guess = Wordle_Reinforcement_Learning.to_word(new_guess[0])
			print(new_word_guess)

			new_enc_guess, done, final_turn = self.wordle_game.advance_state(new_word_guess)

			self.encoded_guesses.append(new_enc_guess)

		if final_turn and (not done):
			state = self.get_state(self.encoded_guesses)
			print(state)
			vocab = Wordle_Reinforcement_Learning.vocab_filter_total(state, self.vocab)
			print(vocab.shape)
			vocab_dist = Wordle_Reinforcement_Learning.get_vocab_distribution(vocab)
			info_list = Wordle_Reinforcement_Learning.word_information(vocab, vocab_dist, state)
			new_guess = max(info_list, key = lambda x: x[1])
			self.local_guesses.append(new_guess)
			max_info_guesses = sorted(info_list, key = lambda x: x[1], reverse = True)
			print([f"{Wordle_Reinforcement_Learning.to_word(w[0])}: {w[1]:.2f}" for w in max_info_guesses[0:10]])
			new_word_guess = Wordle_Reinforcement_Learning.to_word(new_guess[0])
			print(new_word_guess)

			new_enc_guess, done, final_turn = self.wordle_game.advance_state(new_word_guess)
			self.encoded_guesses.append(new_enc_guess)

		print("DONE")

		if self.end_with_close:
			self.wordle_game.driver.quit()

		return sum([i[1] for i in new_enc_guess]) == (3 * 5) # success or not

	def step(self):
		"""
		For playing Wordle Game either locally live or externally manual.
		Largely depricated and does not support ultra instinct

		Modes:
		x - ultra_instinct
		o - manual
		o - debug
		"""
		done = False
		while not done:

			if self.debug:
				inp = input("Continue")

			state = self.get_state(self.encoded_guesses)
			print(state)
			vocab = Wordle_Reinforcement_Learning.vocab_filter_total(state, self.vocab)
			print(vocab.shape)
			# if inp == "vocabs":
			# 	print([Wordle_Reinforcement_Learning.to_word(w) for w in vocab])
			vocab_dist = Wordle_Reinforcement_Learning.get_vocab_distribution(vocab)
			info_list = Wordle_Reinforcement_Learning.word_information(vocab, vocab_dist, state)
			new_guess = max(info_list, key = lambda x: x[1])
			self.local_guesses.append(new_guess)
			new_word_guess = Wordle_Reinforcement_Learning.to_word(new_guess[0])
			print(new_word_guess)

			if self.manual:
				manual_input = input("Insert Encoded String")
				self.update_guesses(manual_input)
				if manual_input == "quit":
					break
			
			if not self.manual:
				new_encoded_guesses, done = self.wordle_game.advance_state(new_word_guess, verbose = self.debug)
				self.encoded_guesses = new_encoded_guesses
		
		print("DONE")

	def to_word(mat):
		"""
		Convert word matrix to string.

		Input: (5, 26) onehot encoded matrix of a 5-letter word

		Output: 5-letter word string
		"""
		return ''.join([string.ascii_lowercase[i] for i in np.argmax(mat, axis = -1).squeeze()])

	def to_onehot(encoded):
		"""
		Convert string to word matrix.

		Input: 5-letter word string

		Output: (5, 26) onehot encoded matrix of a 5-letter word
		"""
		onehot = np.zeros([i for i in encoded.shape] + [len(string.ascii_lowercase)]).reshape(-1, len(string.ascii_lowercase))

		onehot[np.arange(0, onehot.shape[0]), encoded.reshape(-1,)] = 1.

		return onehot.reshape([i for i in encoded.shape] + [len(string.ascii_lowercase)])

	def get_initial_vocab(self, dict_path):
		"""
		Initializing function to get all 5-letter words and write to local variable self.vocab

		Input: path to vocabulary file (JSON)
		"""
		with open(dict_path, "r") as words_read:
			words = json.load(words_read)

		encoded_words = []

		for w in words:
			encoded_words.append([self.letter_dict[l] for l in w])

		encoded_words_numpy = np.array(encoded_words)

		return Wordle_Reinforcement_Learning.to_onehot(encoded_words_numpy)

	def get_zero_out_state(state):
		"""
		Use word-elimination state to create a binary matrix representing all possible letters and positions

		Input: (5,26) letter-position state

		Output: (5, 26) binary matrix of possible letters and positions
		"""
		return np.float32(~np.isin(state, [1., 3.]))
	
	def get_vocab_distribution(vocab):
		"""
		Create a probability matrix representing the vocab distribution of letters in positions

		Input: vocabulary

		Output: (5, 26) probability matrix
		"""
		return vocab.mean(axis = 0)

	def word_information(vocab, vocab_distribution, state):
		"""
		Create a list representing the information to be gained for each word

		Inputs:
		- vocabulary
		- (5, 26) letter and position probability distribution
		- (5,26) letter-position state

		Output: List with each item being a tuple of (onehot encoded word, information value)
		"""
		info_list = []

		for v in vocab:
			info_list.append(Wordle_Reinforcement_Learning.information_gained(v, vocab_distribution, state))
		
		return info_list


	def information_gained(w, vocab_distribution, state):
		# w: (5, 26) word
		"""
		Calculates the information value for a given word

		Inputs:
		- (5, 26) one hot encoded word
		- (5, 26) letter and position probability distribution
		- (5,26) letter-position state

		Output: Tuple containing (onehot encoded word, information value of word)
		"""
		total_info = 0.0

		repeated_letters = set()

		for i in range(w.shape[0]):
			# Probability of new information gained

			l = np.argmax(w[i])

			if state[i, l] == 3:
				continue

			if state[i, l] == 1:
				repeated_letters.add(l)
				continue
			
			if state[i, l] == 2:
				total_info +=  ((vocab_distribution[i, l] * (1. - vocab_distribution[i, l]))) * (l not in repeated_letters)
			else:
				# total_info += ((vocab_distribution[i, l] * 3.) + (vocab_distribution[np.arange(0, w.shape[0]) != i, l].sum() * 2.) + (1. - vocab_distribution[:, l].sum()) * 1.5) * (l not in repeated_letters)

				total_info +=  ((vocab_distribution[i, l] * (1. - vocab_distribution[i, l])) + (vocab_distribution[np.arange(0, w.shape[0]) != i, l].sum() * (1. - vocab_distribution[:, l].sum())) + ((1. - vocab_distribution[:, l].sum()) * vocab_distribution[:, l].sum())) * (l not in repeated_letters)

				repeated_letters.add(l)

		return (w, total_info)


	def update_state(self, state, letter_info):
		"""
		Updates the letter-position state based on the evaluation of a letter

		Inputs:
		- current letter-position state
		- letter info containing:
			- letter
			- position
			- evaluation {3: correct, 2: present, 1: absent}

		Output: updated letter-position state
		"""
		l = self.letter_dict[letter_info[1]]
		position = letter_info[0]
		
		if letter_info[2] == 1:
			if letter_info[3]:
				state[position, l] = 1.
			else:
				state[:, l] = 1.

		if letter_info[2] == 2:
			state[:, l] = 2.
			# state[position, l] = 1.

		if letter_info[2] == 3:
			state[position, :] = 1.
			state[position, l] = 3.
		
		return state

	def sort_updates(updates):
		"""
		Rearrange letter infos for a sequence of state-updating that prevents new guesses to overwrite information from past guesses

		Input: Unordered sequence of updates

		Output: Ordered sequence of updates 
		"""
		sort_2 = [u for u in updates if u[2] == 2]
		sort_1 = [u for u in updates if u[2] == 1]
		sort_3 = [u for u in updates if u[2] == 3]

		return sort_2 + sort_1 + sort_3
	
	def get_state(self, guesses):
		"""
		Create letter-position state based on all current guesses

		Input: encoded guesses

		Output: letter-position state
		"""
		new_state = np.zeros((5, 26))
		all_update_guesses = []
		for g in guesses:

			# For specific scenario where a guess has 2 of the same letters and the truth only has one of the letters,
			# so the first letter guess is present and the update is sorted first
			# but the second letter guess is absent and overwrites the possibility of that letter being in the truth.
			present_letters = set()

			for i, l in enumerate(g):
				all_update_guesses.append((i, l[0], l[1], l[0] in present_letters))
				if l[1] == 2:
					all_update_guesses.append((i, l[0], 1, True))
					present_letters.add(l[0])

		sorted_updates = Wordle_Reinforcement_Learning.sort_updates(all_update_guesses)

		print(sorted_updates)

		for info in sorted_updates:
			new_state = self.update_state(new_state, info)
		
		return new_state

	def vocab_filter_cycle(vocab, condition, p, l):
		"""
		Filters vocabulary based on the evaulation of one letter at one position

		Inputs:
		- current vocabulary
		- evaluation {3: correct, 2: present, 1: absent}
		- position of letter
		- letter

		Output: filtered vocabulary
		"""
		v = np.argmax(vocab, axis = -1)

		if condition == 1:
			return vocab[v[:, p] != l]
		if condition == 2:
			return vocab[(v == l).sum(axis = 1).astype("bool")]
		if condition == 3:
			return vocab[v[:, p] == l]
		
		return vocab

	def vocab_filter_total(state, vocab):
		"""
		Full filter of vocabulary based on every letter-position combination in the letter-position state

		Inputs:
		- letter-position state
		- vocabulary

		Output: fully filtered vocabulary
		"""
		for p in range(state.shape[0]):
			for l in range(state.shape[1]):
				vocab = Wordle_Reinforcement_Learning.vocab_filter_cycle(vocab, state[p, l], p, l)
		return vocab
	

if __name__ == "__main__":
	dict_path = "/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json"
	trish = Wordle_Reinforcement_Learning(dict_path, debug = False, archive = True, live_play = False, ultra_instinct = True, archive_num = 1)
	trish.live_play_ultra()

