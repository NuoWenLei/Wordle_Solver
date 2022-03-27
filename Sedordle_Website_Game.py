from selenium.webdriver import Safari
from selenium.webdriver.common.keys import Keys
import time


class Sedordle_Website_Game():

	def __init__(self, ultra_instinct = False, daily = False):
		self.driver = Safari()
		self.turn = 0
		self.success = 0
		self.lives = 21
		self.guesses = [[] for i in range(self.lives)]
		self.all_encoded_guesses = []
		self.ultra_instinct = ultra_instinct
		self.daily = daily
		self.num_game_boards = 16
		self.completed_boards = [False for i in range(self.num_game_boards)]
		

		self.initialize_quordle()

	def initialize_quordle(self):
		url = "https://sedordle.com/"

		self.driver.get(url)
		self.driver.maximize_window()
		# modal = self.driver.execute_script("return document.getElementsByTagName('game-app')[0].shadowRoot.querySelector('game-modal')")

		# if modal:
		# 	self.driver.execute_script("return document.getElementsByTagName('game-app')[0].shadowRoot.querySelector('game-modal').remove()")

		self.body = self.driver.find_element_by_xpath("//body")

	def advance_state(self, w):

		for n in w.lower():
			time.sleep(.1)
			self.body.send_keys(n)
		time.sleep(1)
		self.body.send_keys(Keys.ENTER)
		time.sleep(1.5)

		encoded_guesses = self.read_state()

		done, success = self.check_finished(encoded_guesses)

		self.turn += 1

		if self.ultra_instinct:
			return encoded_guesses, done, ((self.turn + self.num_game_boards) == self.lives), success
		return encoded_guesses, done

	def check_finished(self, guesses):

		full_sum = 0.

		for i, g in enumerate(guesses):
			temp_sum = 0.
			for l in g:
				full_sum += 3. if type(l[-1]) == str else l[-1]
				temp_sum += 3. if type(l[-1]) == str else l[-1]
			if temp_sum / 5. == 3.:
				self.completed_boards[i] = True


		if full_sum / (5. * self.num_game_boards) == 3.:
			return True, True

		if self.turn == self.lives:
			return True, False

		return False, False

	
	def read_state(self):

		# game_boards = []
		# for i in range(self.num_game_boards):
		# 	game_boards.append(self.driver.execute_script(f"""
		# 	return document.querySelector('div[aria-label=`Game Board {i}`]')
		# 	"""))

		all_enc_guesses = []
		for i in range(self.num_game_boards):
			if self.completed_boards[i]:
				all_enc_guesses.append([[""] for i in range(5)])
				continue
			enc_guess = []
			letters = self.driver.execute_script(f"""
			return document.querySelectorAll("div.chakra-stack.css-6wymoi, div.chakra-stack.css-zu2mh5")[{i}].querySelectorAll("div.chakra-stack.css-84zodg")[{self.turn}].querySelectorAll("div.css-eumhuh, div.css-1m48cht, div.css-ju845e")
			""")
			for l in letters:
				enc_letter = []
				full_evaluation = l.get_attribute("class").strip()
				enc_letter.append(l.get_attribute("textContent").strip().lower())

				# different: 2, incorrect: 1, correct: 3

				if 'css-1m48cht' in full_evaluation:
					enc_letter.append(2)
				
				if 'css-ju845e' in full_evaluation:
					enc_letter.append(1)
				
				if 'css-eumhuh' in full_evaluation:
					enc_letter.append(3)
				
				enc_guess.append(enc_letter)
			
			all_enc_guesses.append(enc_guess)

		return all_enc_guesses






# def setup():
# 	driver = Safari()
# 	driver.get("https://www.nytimes.com/games/wordle/index.html")

# 	modal = driver.execute_script("return document.getElementsByTagName('game-app')[0].shadowRoot.querySelector('game-modal')")

# 	if modal:
# 		driver.execute_script("return document.getElementsByTagName('game-app')[0].shadowRoot.querySelector('game-modal').remove()")

# 	body = driver.find_element_by_xpath("//body")
