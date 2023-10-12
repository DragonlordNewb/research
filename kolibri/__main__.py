from kolibri.all import *

from sys import argv

class Kolibri:
	def __getitem__(self, id: str) -> Callable:
		return getattr(self, "test" + str(id))
	
	def test1(self) -> None:
		st = Spacetime()


if __name__ == "__main__":
	pass