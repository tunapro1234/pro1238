import colorama

__version__ = "0.0.0"
json_indent = 4

keywords_help = {
		"help": "",
		"init": "",
		"pwd": "",
		"cd": "",
		"ls": "",
		"le": "List entry",
		"rm": "",
		"re": "Remove entry",
		"mkdir": "Make directory (Folder)",
		"mksub": "Make Subject",
		"mkent": "Make Entry",
		"clear": "Clear screen",
		"exit": "Exit"
}

database_dependent_keywords = [ 
		"pwd", "cd", "ls", "le", "rm", 
		"re", "mkdir", "mksub", "mkent" 
		]

path_user_keywords = [ 
		"pwd", "cd", "ls", "le", 
		"rm", "re", "mkent" 
		]

keywords = list(keywords_help.keys())

clean = colorama.Style.RESET_ALL
warn = f"[{colorama.Fore.YELLOW	} WARN {colorama.Style.RESET_ALL}]"
info = f"[{colorama.Fore.BLUE	} INFO {colorama.Style.RESET_ALL}]"
fail = f"[{colorama.Fore.RED	} FAIL {colorama.Style.RESET_ALL}]"
ok   = f"[{colorama.Fore.GREEN	}  OK  {colorama.Style.RESET_ALL}]"
bold = '\033[1m'


inpst = f"tunapro1238]{clean}"
folder_color = colorama.Fore.BLUE + bold
# subject_color = colorama.Fore.WHITE
subject_color = colorama.Style.RESET_ALL

def colorize(string, *colors):
	return f"{''.join(colors)}{string}{colorama.Style.RESET_ALL}"

