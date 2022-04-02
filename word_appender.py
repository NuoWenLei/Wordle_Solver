import json

def add_words():
	new_words = ["RAMEN"]
	with open("/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json", "r") as js_words:
		words = json.load(js_words)
	
	print(len(words))
	prev_words = set(words)
	for w in new_words:
		prev_words.add(w.strip().lower())
	
	new_word_set = list(prev_words)

	print(len(new_word_set))

	with open("/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json", "w") as js_words:
		json.dump(new_word_set, js_words)
	
if __name__ == "__main__":
	add_words()
