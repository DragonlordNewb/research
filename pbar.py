
import sys
import time

class ProgressBar:
    def __init__(self, iterable, length=None, fill_char='█', width=40):
        self.iterable = iterable
        self.length = length if length is not None else len(iterable)
        self.fill_char = fill_char
        self.width = width

    def __iter__(self):
        self.progress = 0
        self.iterator = iter(self.iterable)
        return self

    def __next__(self):
        try:
            item = next(self.iterator)
        except StopIteration:
            sys.stdout.write('\n')
            raise StopIteration

        self.progress += 1
        percentage = self.progress / self.length
        filled_width = int(self.width * percentage)
        bar = f'{self.fill_char * filled_width}{" " * (self.width - filled_width)}'
        sys.stdout.write(f'\r[{bar}] {percentage * 100:.1f}%')
        sys.stdout.flush()

        return item

# Example usage:
if __name__ == '__main__':
    items = range(1000)
    progress = ProgressBar(items, width=50)
    for item in progress:
        time.sleep(0.01)
