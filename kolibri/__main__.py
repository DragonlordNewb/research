from kolibri.all import *

from sys import argv

import os

class Kolibri:

	VERSION = "0.0.1"

	def __init__(self) -> None:
		self.st = Spacetime()

	def processCommand(self, cmd: list[str]) -> None:
		match cmd:
			case ("exit" | "quit", *_):
				exit(0)
			case ("sys" | "system", "version" | "ver" | "v"):
				print("This is Kolibri version " + self.VERSION)
			case ("sys", "echo", "{", *words, "}"):
				print(" ".join(words))
			case ("metric", "get", "current"):
				print("Current metric is", self.st.metric)
			case ("metric", "get", "all"):
				print("Getting all available metrics ...")
				for m in metric.engine.Metric.REGISTRATIONS.keys():
					print(" ", m)
				print("Done.")
			case ("metric", "set", newMetric):
				print("Setting current metric ...")
				try:
					m = metric.engine.Metric.lookup(newMetric)
				except KeyError:
					print("Error: no such metric.")
					return
				print("Selected metric is of type " + repr(type(m)) + ".")
				self.st.metric = m
				print("Successfully set metric.")
			case _:
				print("Unknown command.")

if __name__ == "__main__":
	k = Kolibri()
	if len(argv) == 1:
		print("Welcome to the Kolibri command line.")
		print("Enter any command to continue.")
		while True:
			k.processCommand(input(" > ").split(" "))
	else:
		pth = argv[1]
		if not os.path.exists(pth):
			print("File does not exist.")
			exit(1)
		else:
			print("Executing", pth, "...")
			with open(pth, "r") as f:
				for line in f.read().split(";"):
					if line == "":
						continue
					if "-d" in argv:
						print(pth + " > \"" + line.strip() + "\"")
					k.processCommand(line.strip().split(" "))