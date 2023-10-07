class Quecto:
	def commands(self, raw: str) -> list[list[str]]:
		indent = 0
		commands = []
		command = []
		for line in raw.split("\n"):
			for word in line.split(" "):
				match word:
					case "{" | "[" | "(":
						indent += 1
						command.append(word)
					case "}" | "]" | ")":
						indent -= 1
						command.append(word)
					case ";" if indent == 0:
						commands.append(command)
						command = []
					case _:
						command.append(word)
