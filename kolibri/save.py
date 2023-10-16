import kolibri
from kolibri.utils import *

class Save:
	CLASSIFICATIONS = {}

	def __init__(self, f: str) -> None:
		self.tf = f
		self.f = None
		self.opened = False

	def openFile(self) -> None:
		self.f = open(self.f)
		self.opened = True

	def closeFile(self) -> None:
		if self.opened:
			self.f.close()
			self.f = None
			self.opened = False

	def __bool__(self) -> bool:
		return self.opened

	@classmethod
	def classify(cls, name: str) -> type:
		def deco(ncls):
			Save.CLASSIFICATIONS[name] = ncls
			return ncls
		return deco
	
	@classmethod
	def importClass(cls, name: str) -> type:
		return cls.CLASSIFICATIONS[name]
	
	@classmethod
	def exportClass(cls, targetClass: type) -> str:
		for index, t in enumerate(cls.CLASSIFICATIONS.values()):
			if t == targetClass:
				return cls.CLASSIFICATIONS.keys()[index]
		raise KeyError("No such type classified.")
	
	def __rshift__(self, obj: object) -> str:
		