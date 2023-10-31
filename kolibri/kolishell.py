from sys import argv
from kolibri import constants
from kolibri import entity
from kolibri import force
from kolibri import metric
from kolibri import spacetime
from kolibri import utils
from kolibri.utils import *

class Kolishell:

	BANNER = "Welcome to the Kolibri shell.\nType any command to continue."
	PREFIX = " > "
	
	def __init__(self) -> None:
		self.spacetime = spacetime.Spacetime()

	def processCommand(self, cmd: str) -> None:
		match cmd.strip().split(" "):
			case ("f" | "fetch", datatype):
				if datatype in ("e", "entity"):
					print("Fetching available entity types ...")
					for key in entity.Entity.REGISTRATIONS.keys():
						print(" -", key)
					print("Done.")
				elif datatype in ("m", "metric"):
					print("Fetching available metrics ...")
					for key in metric.Metric.REGISTRATIONS.keys():
						print(" -", key)
					print("Done.")
				elif datatype in ("f", "i", "force", "forces", "field", "interaction", "fields", "interactions"):
					print("Fetching available interactions and fields ...")
					for key in force.Force.REGISTRATIONS.keys():
						print(" -", key)
					print("Done.")
				else:
					print("No such data type \"" + datatype + "\".")

			case ("s" | "search", datatype):
				print("Searching all registries for \"" + datatype + "\" ...")
				datatype = datatype.lower()
				hit = False
				for key in entity.Entity.REGISTRATIONS.keys():
					if datatype in key:
						print("  Hit:", key, "is an available entity type.")
						hit = True
				for key in metric.Metric.REGISTRATIONS.keys():
					if datatype in key:
						print("  Hit:", key, "is an available metric.")
						hit = True
				for key in force.Force.REGISTRATIONS.keys():
					if datatype in key:
						print("  Hit:", key, "is an available force.")
						hit = True
				if not hit:
					print("No results.")

			case ("execf", filename):
				with open(filename, "r") as f:
					for cmd in f.read().split("\n"):
						self.processCommand(cmd)

			case ("rem" | "#" | "//", *_):
				pass
				
			case ("quit" | "exit", *_):
				exit(0)

			case _:
				print("Invalid or incomplete command:", cmd)

	def trace(self, eid: str, ticks: int) -> None:
		ent: entity.Entity = None
		for possibleEntity in self.spacetime.entities:
			if possibleEntity.id == eid:
				ent = possibleEntity
				break
		if ent is None:
			print("Error: no such entity.")
			return 1
		for _ in range(ticks):
			print(eid, "- at", repr(eid.location), "with velocity", repr(eid.velocity))
			self.spacetime.tick(1)

	def cli(self) -> None:
		print(self.BANNER)
		try:
			while True:
				try:
					self.processCommand(input(self.PREFIX))
				except KeyboardInterrupt:
					exit(0)
		except KeyboardInterrupt:
			exit(0)