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
			case ("sys" | "system", "st" | "spacetime"):
				print("Spacetime object is", self.st)
			case ("sys" | "system", "echo" | "print", "{", *words, "}"):
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
			case ("body", "add" | "+", t, name, "{", *kwargs, "}", "at", x, y, z):
				print("Assembling body ...")
				try:
					bodyType = body.engine.Body.lookup(t)
				except KeyError:
					print("Error: no such body type.")
					return
				kwargs = {i.split("=")[0]: Decimal(i.split("=")[1]) for i in kwargs}
				l = Vector(Decimal(x), Decimal(y), Decimal(z))
				b = bodyType(name, l, **kwargs)
				self.st.bodies << b
				print("Body successfully assembled.")
			case ("body", "locate", id):
				for b in self.st.bodies:
					if b.id == id:
						print(id, "is located at", b.location)
						return
				print("No such body.")
			case ("field", "add" | "+", t, "{", *kwargs, "}"):
				print("Adding field ...")
				try:
					fieldType = field.engine.Field.lookup(t)
				except KeyError:
					print("Error: no such body type.")
					return
				kwargs = {i.split("=")[0]: Decimal(i.split("=")[1]) for i in kwargs}
				f = fieldType(**kwargs)
				self.st.fields << f
				print("Field successfully added.")
			case ("tick", x):
				if self.st.metric == None:
					print("Can\'t tick without a metric.")
					return
				print("Ticking ...")
				self.st.tick(int(x), pbar=True)
			case ("trace", id, x):
				if self.st.metric == None:
					print("Can\'t tick without a metric.")
					return
				targetBody = None
				for b in self.st.bodies:
					if b.id == id:
						targetBody = b
						break
				if targetBody == None:
					print("No such body.")
					return
				for _ in range(int(x)):
					self.st.tick()
					print("\r", id, "is at", targetBody.location, end="                 ")
				print("\n", end="")
			case _:
				print("Unknown or invalid command:", " ".join(cmd))

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
