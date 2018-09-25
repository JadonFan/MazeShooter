import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt 
import os

mpl.style.use("classic")


def set_resource(filename):   
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def read_csv(filename):
	game_round = 1
	stat_code = 1 

	with open(filename) as f:
		content = f.readlines()

		for line in content:
			line.strip()
			stat_code += 0

			if line[0] == "%":      # indicates statistics for a new game is to be read 
				game_round = line[1]   # the number following the % is the game round number, i.e., which previous number is being referred
				stat_code = 1   # refers to the statistic that each line keeps track of (for now, only one stat_code exists, which is 1 for KO_count per level)
			elif not line.isEmpty():
				for char in line:
					if char.isDigit():
						x = "placeholder"


# plot_numberkilled(KO_count, max_level, other_games = []) plots a line graph indicating the number of enemies killed each level, up to max_level
# for the current game round and, when other_games is not empty, for other game rounds too.
def plot_numberkilled(KO_count, max_level, other_games = []): 
	levels = np.arange(1, max_level + 1)
	plt.plot(levels, KO_count, linewidth = 5)

	plt.title("KOs Per Level")
	plt.xlabel("Level")
	plt.ylabel("KO Count")
	plt.grid(True, "major", color = '0.5')
	plt.grid(True, "minor", color = '0.25')

	greatest_KOs = max(KO_count)
	plt.xticks(np.arange(1, max_level + 2, step = 1.0))
	plt.yticks(np.arange(0, max(KO_count) + 2, step = np.ceil(greatest_KOs/10)))

	plt.rcParams["axes.edgecolor"] = "black"
	plt.rcParams["axes.linewidth"] = 0.5

	plt.gcf().set_size_inches(10, 10)
	plt.savefig(set_resource("levelKO.png"), dpi = plt.gcf().dpi)
