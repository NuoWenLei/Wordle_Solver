from Semantle_Website_Game import Semantle_Website_Game
from tqdm import tqdm
import numpy as np
import json

class Semantle_Solver():

	def __init__(self, num_landmarks = 5, allowed_guesses = 50, struggle = False, digits = 2):

		with open("embed_vec_filtered.npy", "rb") as filtered_npy_reader:
			self.word_embedding = np.load(filtered_npy_reader)

		with open("filtered_word2index.json", "r") as filtered_json_reader:
			self.word_list = np.array(json.load(filtered_json_reader))
			
		self.word2index = dict((w, i) for i, w in enumerate(self.word_list))

		self.game = Semantle_Website_Game(struggle, digits)

		self.landmark_words = np.random.choice(self.word_list, size = num_landmarks, replace = False)

		print(self.landmark_words)

		self.landmark_similarities = []

		self.guessed_indices = []

		self.all_indices = np.array([i for i in range(len(self.word_list))])

		self.SIM_ERROR_MATRIX = np.zeros((len(self.word_list), 1))

		self.allowed_guesses = allowed_guesses

	def guess_landmarks(self):
		for w in tqdm(self.landmark_words):
			sim_score, _, done = self.game.advance_state(w)

			if done:
				Exception(f"Landmark {w} is the word?!")

			self.landmark_similarities.append(sim_score)

			self.calc_similarity_diffs(w, sim_score)
		
		print(self.landmark_similarities)

	def calc_similarity_diffs(self, word, sim_score):
		word_vector = self.word_embedding[self.word2index[word]]

		vec_sims = self.cosine_similarity(word_vector, self.word_embedding)

		adjusted_sim_abs = np.abs(vec_sims - sim_score)

		self.SIM_ERROR_MATRIX = self.SIM_ERROR_MATRIX + adjusted_sim_abs

	def normalize(self, v):
		norm=np.linalg.norm(v, axis = -1)
		norm += np.float32(norm == 0.)
		return norm

	def cosine_similarity(self, x, y):
		x_norm = self.normalize(x)
		y_norm = self.normalize(y)

		return (np.sum(x * y, axis = -1) / (x_norm * y_norm))[..., np.newaxis]

	def live_play(self):

		print("Guessing Landmarks...")

		self.guess_landmarks()

		print("Beginning Actual Guesses")

		total_guesses = 0
		
		while self.allowed_guesses > 0:
			
			# Find current guess
			current_guess_index = int(np.argmin(self.SIM_ERROR_MATRIX))
			current_guess = self.word_list[current_guess_index]

			# Guess
			print(f"Guessing {current_guess} with index {current_guess_index}")
			sim_score, sim_validity, done_check = self.game.advance_state(current_guess)
			if sim_validity:
				print(sim_score)
				total_guesses += 1

			# If done, print results
			if done_check:
				print(f'Success! Word is {current_guess}!!! Guessed in {total_guesses} attempts after landmark')
				break

			# Add high value to similarity error of current guess
			# to ensure this index is not guessed again
			self.SIM_ERROR_MATRIX = self.SIM_ERROR_MATRIX + (np.float32(self.all_indices == current_guess_index) * 1000.)[..., np.newaxis]

			if sim_validity:
				# If not done and word exists, update similarity error matrix
				self.calc_similarity_diffs(current_guess, sim_score)

				# decrement allowed guesses
				self.allowed_guesses -= 1

		if self.allowed_guesses == 0:
			print(f"Failed after {total_guesses} allowed attempts")


if __name__ == "__main__":
	solver = Semantle_Solver(
		num_landmarks = 5,
		allowed_guesses = 50,
		struggle=True,
		digits = 1
	)
	solver.live_play()