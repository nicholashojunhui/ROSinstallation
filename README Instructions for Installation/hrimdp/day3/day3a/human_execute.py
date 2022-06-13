import sys

from utility import *
from gridworld import GridWorld

from rewards import *

dic_actions = {'L': [0,-1], 'R': [0,1], 'U': [-1,0], 'D': [1,0], 'S': [0,0], 'T': [0,0]}

def human_execute(gridworld, init_state, actions):
	human_states = []

	if gridworld.is_wall(init_state[0][0], init_state[0][1]):
		return None
	human_states.append(init_state)

	current_cell = init_state[0]
	current_request = init_state[1]
	current_action = None
	for action in actions:
		current_move = dic_actions[action]
		next_cell = [c + a for c, a in zip(current_cell, current_move)]

		if not gridworld.is_wall(next_cell[0], next_cell[1]):
			current_cell = next_cell

		current_request = current_request if action is not 'T' else (1 - current_request)

		human_states.append([current_cell, current_request])
	return human_states

if len(sys.argv) != 7:
	print()
	print("usage: python3 human_exectue.py gridworld.csv actions.csv init_x init_y init_request output.csv")
	exit()

gridworld_filename = sys.argv[1]
actions_filename = sys.argv[2]
init_x = int(sys.argv[3])
init_y = int(sys.argv[4])
init_request = int(sys.argv[5])

output_filename = sys.argv[6]


gridworld = load_gridworld(gridworld_filename)
actions = load_actions(actions_filename)

human_states = human_execute(gridworld, [[init_x, init_y], init_request], actions)

print(human_states)

record_human_states(output_filename, human_states)
