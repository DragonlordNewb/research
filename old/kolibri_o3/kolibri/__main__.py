from kolibri import kolishell
from sys import argv

if __name__ == "__main__":
	ks = kolishell.Kolishell()
	if len(argv) > 1:
		cmd = " ".join(argv[1:])
		print(" >", cmd)
		ks.processCommand(cmd)
	else:
		ks.cli()