print("Loading STEM1 ...")

from stem1 import *

colors = utils.Colors()

print(colors.fg.lime + "Space-Time Engineering Miniature v1 loaded successfully." + colors.reset)
print("Enter any command to continue.")

while True:
	usr = input(" > ")
	match usr.split(" "):
		case ("exit", *_):
			print(colors.fg.red + "Exiting ..." + colors.reset)