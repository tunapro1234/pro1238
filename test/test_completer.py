import database
import readline


keywords_help = {
		"help": "",
		"init": "",
		"pwd": "",
		"cd": "",
		"ls": "",
		"le": "List entry",
		"rm": "",
		"re": "Remove entry",
		"add": "Same with makes",
		"mkdir": "Make directory (Folder)",
		"mksub": "Make Subject",
		"mkent": "Make Entry",
		"clear": "Clear screen"
}

commands = list(keywords_help.keys())
command_args = ["subject", "folder", "data"]
keywords = commands + command_args


def complete_path(db, selected, word):
	if selected is None or db is None: return []
	base = db if word.startswith("/") else selected

	names = [i for i in word.split("/") if i != ""]
	names = names if word.endswith("/") else names[:-1]
	nbase = base
	for name in names:
		nbase = nbase.find_by_name(name)

	beg = "/".join(word.split("/")[:-1])
	beg = beg if beg == "" else beg + "/"
	return [beg + e for e in nbase.list_sub_names()]

def completer_wrapper(db, selected):
	selected = db if selected is None else selected

	def completer(text, state):
		words = readline.get_line_buffer().split(" ")
		vocab = []

		if len(words) == 1:
			vocab = commands

		if words[0] == "add":
			if len(words) == 2:
				vocab = command_args
			elif len(words) == 3:
				vocab = complete_path(db, selected, words[2])

		if selected is not None and words[0] in ["ls", "rm", "cd"]:
			vocab = complete_path(db, selected, words[1])
			# print(f"vocab: {vocab}")
			
		results = [i for i in vocab if i.startswith(text)] + [None]
		return results[state]
	return completer

def completer_foo(db, selected, text):
	words = text.split(" ")
	vocab = []

	if len(words) == 1:
		vocab = commands

	if words[0] == "add":
		if len(words) == 2:
			vocab = command_args
		elif len(words) == 3:
			vocab = complete_path(db, selected, words[2])

	if len(words) == 2 and selected is not None and words[0] in ["ls", "rm", "cd"]:
		vocab = complete_path(db, selected, words[1])
		
	results = [i for i in vocab if i.startswith(words[-1])] + [None]
	return results

def main():
	readline.parse_and_bind("tab: complete")
	# readline.set_completer(completer_wrapper(None, None))

	db = database.default_structure
	selected = db
	
	while True:
		readline.set_completer(completer_wrapper(db, selected))
		inp = input(f"tunapro1238] >> ")
		rv = completer_foo(db, selected, inp)
		print(rv)
# 		rv = complete_path(db, selected, inp)
# 		print([i for i in rv if i.startswith(inp)])


if __name__ == "__main__":
	main()
