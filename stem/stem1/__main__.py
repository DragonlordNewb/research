# Space-Time Engineering Miniature.

VERSION = "1.0.0"

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
			exit(0)

		case ("sys", command, *args):
			match [command] + list(args):
				case ("--version", *_):
					print("This is " + colors.fg.lime + "Space-Time Engineering Miniature version " + VERSION + colors.reset + ".")

				case ("--list", "metrics"):
					print("Getting list of available metrics ...")
					metrics = list(engine.Metric.REGISTRATIONS.keys())
					print(colors.fg.lime + "List of available metrics acquired:" + colors.reset)
					for metric in metrics:
						print("  " + metric)