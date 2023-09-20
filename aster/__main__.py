from aster.utils import ColorPrinter

cpt = ColorPrinter() # Color printer!

cpt("Loading ...", cpt.fg.yellow)

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