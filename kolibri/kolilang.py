from kolibri.utils import *

from sys import argv

class Kolilang1Interpreter:
	
	VARIABLES = {}
	TYPE_LABELS = {
		"num": Decimal,
		"str": str
	}

	def __init__(self, **parameters) -> None:
		self.PARAMETERS = parameters
		for key in parameters:
			if parameters[key].isnumeric():
				v = Decimal(parameters[key])
			self.VARIABLES[key] = v

	def executeLine(self, line: str) -> None:
		match line.split(" "):
			case ("expect", "{", t, name, "}"):
				if name in self.PARAMETERS.keys():
					if type(self.PARAMETERS[name]) == self.TYPE_LABELS[t]:
						print("Got expected parameter " + name + ".")
					else:
						print("Error 1: Got expected parameter " + name + " of wrong type (needs a " + t + ").")
						exit(1)
				else:
					print("Error 2: Missing expected parameter " + name + ".")
					exit(2)