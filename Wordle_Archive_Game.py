from selenium.webdriver import Safari
from selenium.webdriver.common.keys import Keys
import time


class Wordle_Archive_Game():

	def __init__(self, archive_num, ultra_instinct = False):
		self.driver = Safari()
		self.turn = 0
		self.success = 0
		self.lives = 6
		self.guesses = [[] for i in range(self.lives)]
		self.encoded_guesses = []
		self.ultra_instinct = ultra_instinct
		self.archive_num = archive_num
		

		self.initialize_wordle()

	def initialize_wordle(self):
		print(f"https://www.devangthakkar.com/wordle_archive/?{self.archive_num}")
		self.driver.get(f"https://www.devangthakkar.com/wordle_archive/?{self.archive_num}")

		self.driver.maximize_window()

		time.sleep(5)

		self.driver.execute_script("return document.querySelector('div.ReactModalPortal').remove()")

		self.body = self.driver.find_element_by_xpath("//body")

	def advance_state(self, w):

		for n in w.lower():
			time.sleep(.1)
			self.body.send_keys(n)
		time.sleep(1)
		self.body.send_keys(Keys.ENTER)
		time.sleep(5)

		encoded_guess = self.read_state()

		done = self.check_finished(encoded_guess)

		self.turn += 1

		if self.ultra_instinct:
			return encoded_guess, done, ((self.turn + 1) == self.lives)
		return encoded_guess, done

	def check_finished(self, guess):
		if self.turn == self.lives:
			return True
		
		print(guess)
		if sum([l[-1] for l in guess]) / 5. == 3.:
			return True

		return False

	
	def read_state(self):
		letters = self.driver.execute_script(f"""
		return document.querySelectorAll('div.grid.grid-cols-5.grid-flow-row.gap-4')[0].querySelectorAll('span')
		""")


		enc_guess = []

		for l in letters[(self.turn * 5): ((self.turn + 1) * 5)]:
			enc_letter = []
			enc_letter.append(l.get_attribute("innerHTML").strip().lower())

			evaluation = l.get_attribute("class").strip().split(" ")[0]

			if evaluation == "nm-inset-yellow-500":
				enc_letter.append(2)
			
			if evaluation == "nm-inset-n-gray":
				enc_letter.append(1)
			
			if evaluation == "nm-inset-n-green":
				enc_letter.append(3)
			
			enc_guess.append(enc_letter)

		return enc_guess

		# letters[0].get_attribute("letter")

		# letters[0].get_attribute("evaluation")

		# present: 2, absent: 1, correct: 3






# def setup():
# 	driver = Safari()
# 	driver.get("https://www.nytimes.com/games/wordle/index.html")

# 	modal = driver.execute_script("return document.getElementsByTagName('game-app')[0].shadowRoot.querySelector('game-modal')")

# 	if modal:
# 		driver.execute_script("return document.getElementsByTagName('game-app')[0].shadowRoot.querySelector('game-modal').remove()")

# 	body = driver.find_element_by_xpath("//body")
