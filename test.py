class x:
	@classmethod
	def deco(cls):
		def wrapper(f):
			print("Hello World", f)
			return f
		return wrapper

	@
	def go(self):
		print("hi")