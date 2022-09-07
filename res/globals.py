import colorama

__version__ = "0.0.0"

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


clean = colorama.Style.RESET_ALL
warn = f"[{colorama.Fore.YELLOW} WARN {colorama.Style.RESET_ALL}]"
info = f"[{colorama.Fore.BLUE} INFO {colorama.Style.RESET_ALL}]"
fail = f"[{colorama.Fore.RED} FAIL {colorama.Style.RESET_ALL}]"

folder_color = colorama.Fore.BLUE
# subject_color = colorama.Fore.WHITE
subject_color = colorama.Style.RESET_ALL

def colorize(color, string):
	return f"{color}{string}{colorama.Style.RESET_ALL}"

