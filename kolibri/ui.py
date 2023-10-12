# Make sure Tkinter is installed 

import os
import platform

PY = "py" if platform.system() == "Windows" else "python3"

# a command to install tk if it's not installed, as quiet as possible
command = PY + " -m pip install tk -q -q -q --no-warn-script-location"
result = os.system(command)

if result != 0:
	raise RuntimeError("Tkinter could not be installed and is required for the Kolibri UI.")

del os
del platform