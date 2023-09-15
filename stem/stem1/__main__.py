# Space-Time Engineering Miniature.

VERSION = "1.0.0"

print("Loading STEM1 ...")

from stem1 import *

colors = utils.Colors()

print(colors.fg.lime + "Space-Time Engineering Miniature v1 loaded successfully." + colors.reset)
print("Enter any command to continue.")

st: engine.Spacetime = None
ts: float = None
mt: engine.Metric = None
forces: list[engine.Force] = []

while True:
	usr = input(" > ")
	match usr.split(" "):
		case ("exit", *_):
			print(colors.fg.red + "Exiting ..." + colors.reset)
			exit(0)

		case ("sys", *args):
			match args:
				case ("--version", *_):
					print("This is " + colors.fg.lime + "Space-Time Engineering Miniature version " + VERSION + colors.reset + ".")

				case ("--list", "metrics"):
					print("Getting list of available metrics ...")
					metrics = list(engine.Metric.REGISTRATIONS.keys())
					print(colors.fg.lime + "List of available metrics acquired:" + colors.reset)
					for metric in metrics:
						print("  " + metric)

		case ("config", *args):
			match args:
				case ("--timestep", value):
					print("Configuring simulation timestep ...")
					try:
						ts = float(value)
						print(colors.fg.lime + "Successfully set timestamp." + colors.reset)
					except:
						print(colors.fg.red + "Error: could not set value; make sure value is a float.")
				case ("--metric", name):
					print("Configuring simulation metric ...")
					if name not in engine.Metric.REGISTRATIONS.keys():
						print(colors.fg.red + "Error: unknown metric." + colors.reset)
						continue
					mt = engine.Metric.REGISTRATIONS[name]
					print(colors.fg.lime + "Successfully set metric." + colors.reset)