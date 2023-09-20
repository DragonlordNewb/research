from typing import Callable

from aster.utils import ColorPrinter

__version__ = "0.0.1"

cpt = ColorPrinter() # Color printer!

cpt("Loading ...", cpt.fg.lime)

cpt("  Loading aster.constants ...", cpt.fg.yellow, end="")
from aster import constants
cpt("\r  aster.constants successfully loaded.", cpt.fg.lime)

cpt("  Loading aster.engine ...", cpt.fg.yellow, end="")
from aster import engine
cpt("\r  aster.engine successfully loaded.", cpt.fg.lime)

cpt("  Loading aster.utils ...", cpt.fg.yellow, end="")
from aster import utils
cpt("\r  aster.utils successfully loaded.", cpt.fg.lime)

cpt("Advanced SpaceTime Engineering Research software loaded successfully!", cpt.fg.lime)
cpt("Command line interface loading now ... Type any command, or \"help\" for a list of commands.")

while True:
	try:

		cmd = input(" > ").split(" ")

		match cmd:
			case ("exit", *_):
				cpt("Exiting ...", cpt.fg.red)
				exit()

			case ("sys", "version"):
				cpt("This is Advanced SpaceTime Engineering Research software version " + __version__ + ".")

			case _:
				cpt("Invalid command", cpt.fg.red)

	except KeyboardInterrupt:
		continue