from efesolver.metric import Metric
from efesolver.variables import *

M = newVariable("M")

Fs = (1 - ((2 * G * M) / (r * c2))) * c2
iFs = c2 / Fs

m = Metric([Fs, 0, 0, 0], [0, iFs, 0, 0], [0, 0, iFs, 0], [0, 0, 0, iFs], True)
print(m.scalar())