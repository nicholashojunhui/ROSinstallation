import sys

from utility import *

import random
import numpy as np

def random_actions(seed, timestamps):
	actions = []

	random.seed(seed)
	np.random.seed(seed)

########## to be completed; replace XXXX with correct terms ##########

	# make sure human actions follow the probabilities set in the hrimdp model
	human_actions = [XXXX]
	human_prop = [XXXX]
	actions = np.random.choice(human_actions, timestamps, human_prop).tolist()

######################################################################

	return actions

if len(sys.argv) != 4:
	print()
	print("usage: python3 random_human_actions.py seed timestamps output_human_actions.csv")
	exit()

seed = int(sys.argv[1])
timestamps = int(sys.argv[2])
actions_filename = sys.argv[3]

actions = random_actions(seed, timestamps)
print(actions)
record_human_actions(actions_filename, actions)
