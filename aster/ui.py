print("Advanced SpaceTime Engineering Research software starting up ...")

print("  Loading sys ...", end="")
import sys
print("\r  Completed loading sys.\n  Loading aster.core ...", end="")
from aster.core import *
print("\r  Completed loading aster.core.\n  Loading aster.engine ...", end="")
from aster.engine import *
print("\r  Completed loading aster.engine.\n  Loading aster.real ...", end="")
from aster.real import *
print("\r  Completed loading aster.real.\nASTER successfully loaded!\n")

if len(sys.argv) < 2:

	spacetime = None

	while spacetime == None:
		usr = input("Enter a simulation resolution: ")
		if usr.isnumeric():
			spacetime = Spacetime(int(usr))
			break
		else:
			print("Invalid simulation resolution. Must be an integer.")

else:

	if sys.argv[1].isnumeric():
		spacetime = Spacetime(int(sys.argv[1]))
	else:
		print("Invalid simulation resolution. Must be an integer.")
		exit(1)

	print("Simulation resolution selected: " + sys.argv[1])

print("\nEnter any command to continue.")

def executeCommand(usr):
	try:
		match usr.split(" "):
			case ("exit", *_):
				print("Exiting.")
				exit(0)

			case ("echo", *s):
				print(" ".join(s))

			case ("exec", filename):
				if not os.path.exists(filename):
					print("File not found.")
				elif not os.path.isfile(filename):
					print(filename + " exists but is not a file.")
				else:
					print("Executing \"" + filename + "\" ...")
					with open(filename, "r") as f:
						for cmd in f.read().split(" "):
							executeCommand(cmd)
					print("Finished executing " + filename + "\".")

			case ("clear", *_):
				print("\n" * 500)

			case ("cls", *_):
				print("\n" * 500)

			case _:
				print("Invalid or incomplete command.")

	except KeyboardInterrupt:
		print("Exiting.")
		exit(0)

while True:
	executeCommand(input(" ? "))
