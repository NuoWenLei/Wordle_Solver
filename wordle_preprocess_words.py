import json

def main():
	dict_path = "/Users/nuowenlei/Desktop/Desktop - Old MacBook/School/Concord/G10_Sem1/Adv_CompSci/Eclipse Projects/14-Arrays/dictionary.txt"
	save_path = "/Users/nuowenlei/Desktop/Programming/Python/Wordle_cuz_why_not/five_letter_words.json"
	with open(dict_path, "r") as txt:
		text = txt.readlines()
	
	five_letter_words = [t.strip().lower() for t in text if len(t.strip()) == 5]

	print(len(five_letter_words))

	with open(save_path, "w") as write_txt:
		json.dump(five_letter_words, write_txt)

if __name__ == "__main__":
	main()
