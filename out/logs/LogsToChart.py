import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from os import getcwd
# put filepath of logfile here if you wish to process one log
SINGLE_FILE = ""


def log_to_plt(logfile_path: str):
	log_file = open(logfile_path)
	data = log_file.read()
	lines = data.split('\n')
	no_games = int(lines[0].split('(')[1].split(' ')[0])
	names = []
	labels = []
	scores = []
	i = 2
	while '%' in lines[i]:
		parts = lines[i].split(':')
		names.append(parts[0].lstrip(' '))
		split = parts[1].split(' ')
		scores.append(int(split[1]))
		raw_percent = split[2].strip('(').strip(')').strip('%')
		percent = round(float(raw_percent), 2)
		labels.append(str(scores[i - 2]) + " (" + str(percent) + "%)")
		i += 1
	plt.pie(scores, labels=labels)
	title = ""
	if names[len(names) -1] == "Draws":
		title += names[0] + " Vs. " + names[1]
	else:
		for i in range(0, len(names)):
			if i < len(names) - 1:
				title += names[i] + " Vs. "
			else:
				title += names[i]
	title += "(" + str(no_games) + ")"
	plt.title(title)
	plt.legend(names, loc=2, bbox_to_anchor=(0.95, 0.6))
	plt.savefig("../figs/" + logfile_path.rstrip(".txt") + ".png", bbox_inches='tight')
	plt.show()


if SINGLE_FILE == "":
	files = [f for f in listdir(getcwd()) if isfile(join(getcwd(), f))]
	for file in files:
		if ".txt" in file:
			log_to_plt(file)
else:
	log_to_plt(SINGLE_FILE)
