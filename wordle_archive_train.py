from wordle_reinforcement_learning import Wordle_Reinforcement_Learning

def main(start_from = 0):
	number = 269

	success_states = []

	for i in range(start_from, number):
		dict_path = "/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json"
		trish = Wordle_Reinforcement_Learning(dict_path, debug = False, archive = True, live_play = False, ultra_instinct = True, archive_num = i + 1, end_with_close=True)
		success = trish.live_play_ultra()
		print(success)
		success_states.append(success)

	print("Fails:")
	for i, s in enumerate(success_states):
		if not s:
			print(i)
	
	print(f"Success rate: {float(sum([int(i) for i in success_states])) / float(len(success_states)):.4f}")


if __name__ == "__main__":
	main(start_from = 37)
