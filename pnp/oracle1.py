from typing import Union
from abc import abstractmethod
from abc import ABC

class Clause(ABC):

	"""
	The abstract representation of a Clause.

	For example,

		c = AND(x=True, y=True, z=False)

	is equivalent to "x and y and not z".
	"""

	def __init__(self, **terms: dict[str, bool]) -> None:
		self.terms = terms

	def __getitem__(self, variable: str) -> bool:
		return self.terms[variable]

	@abstractmethod
	def solve(self) -> tuple[dict[str, bool], dict[str, bool]]:
		raise NotImplementedError # how did you even call this function anyway

class AND(Clause):
	def solve(self):
		return self.terms, None

class OR(Clause):
	def solve(self):
		return None, {v: not self[v] for v in self.terms}

class Statement:
	def __init__(self, 
