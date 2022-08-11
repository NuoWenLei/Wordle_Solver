from selenium.webdriver import Safari
from selenium.webdriver.common.keys import Keys
import numpy as np
import time


class Semantle_Website_Game():

	def __init__(self, struggle, digits = 2):
		self.driver = Safari()
		self.turn = 0
		self.guesses = []
		self.struggle = struggle
		self.digits = digits

		self.initialize_semantle()

	def initialize_semantle(self):
		self.driver.get("https://semantle.com/")
		print("Initializing Semantle...")
		time.sleep(10)
		self.driver.execute_script("document.getElementById('rules-underlay').remove()")
		print("Removing Rules Pop-up...")
		time.sleep(3)
		self.guesser = self.driver.execute_script("return document.getElementById('guess')")
	
	def clear_input(self):
		self.driver.execute_script("document.getElementById('guess').value = ''")

	def advance_state(self, w):

		self.clear_input()

		self.guesser.send_keys(w)
		time.sleep(.5)
		self.guesser.send_keys(Keys.ENTER)
		time.sleep(2)

		guess_similarity, sim_validity = self.read_state()

		self.guesses.append([w, guess_similarity, sim_validity])

		done = self.check_finished(guess_similarity)

		self.turn += 1

		return guess_similarity, sim_validity, done

	def check_finished(self, guess_similarity):
		if guess_similarity == 1.:
			return True
		return False

	
	def read_state(self):
		sim_validity = self.driver.execute_script("return document.getElementById('error').innerHTML == ''")
		similarity = self.driver.execute_script("return document.getElementById('guesses').getElementsByTagName('tr')[1].getElementsByTagName('td')[2].innerHTML")

		if self.struggle:

			# 2 digits
			if self.digits == 2:
				return np.float32(int(float(similarity))) / 100., sim_validity

			# 1 digit
			if self.digits == 1:
				return np.float32(int(float(similarity) / 10.)) / 10., sim_validity
		return np.float32(similarity) / 100., sim_validity