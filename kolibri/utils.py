import sys

class ProgressBar:
	def __init__(self, iterable, total=None, length=50, prefix='Progress:', suffix='', fill='█', print_end='\r'):
		self.iterable = iterable
		self.total = total if total is not None else len(iterable)
		self.length = length
		self.prefix = prefix
		self.suffix = suffix
		self.fill = fill
		self.print_end = print_end
		self.current_iteration = 0
	
	def update(self, progress):
		filled_length = int(self.length * progress // self.total)
		bar = self.fill * filled_length + '-' * (self.length - filled_length)
		percent = progress / self.total * 100
		self.print(f'{self.prefix} |{bar}| {percent:.2f}% {self.suffix}', end=self.print_end)
	
	def print(self, text, end='\n'):
		sys.stdout.write(text)
		sys.stdout.flush()
		sys.stdout.write(end)
		sys.stdout.flush()
	
	def __iter__(self):
		for item in self.iterable:
			yield item
			self.current_iteration += 1
			self.update(self.current_iteration)
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		sys.stdout.write('\n')  # Move to the next line after the progress bar is complete
