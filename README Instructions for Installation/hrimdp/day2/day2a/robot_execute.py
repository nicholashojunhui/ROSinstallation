import sys

from utility import *
from gridworld import GridWorld

from rewards import *

dic_actions = {'L': [0,-1], 'R': [0,1], 'U': [-1,0], 'D': [1,0], 'S': [0,0]}

def robot_execute(gridworld, init_state, actions):
	robot_states = []

	if gridworld.is_wall(init_state[0], init_state[1]):
		return None
	robot_states.append(init_state)

	current_state = init_state
	current_action = None
	for action in actions:
		current_action = dic_actions[action]
		next_state = [c + a for c, a in zip(current_state, current_action)]

		if not gridworld.is_wall(next_state[0], next_state[1]):
			current_state = next_state

		robot_states.append(current_state)
	return robot_states

def record_robot_states(filename, robot_states):
	with open(filename, 'w', newline='') as f:
		writer = csv.writer(f, delimiter=',')
		for state in robot_states:
			writer.writerow([state[0], state[1]])

if len(sys.argv) != 6:
	print()
	print("usage: python3 robot_exectue.py gridworld.csv actions.csv init_x init_y output.csv")
	exit()

gridworld_filename = sys.argv[1]
actions_filename = sys.argv[2]
init_x = int(sys.argv[3])
init_y = int(sys.argv[4])

output_filename = sys.argv[5]

gridworld = load_gridworld(gridworld_filename)
actions = load_actions(actions_filename)

robot_states = robot_execute(gridworld, [init_x, init_y], actions)

print(robot_states)

record_robot_states(output_filename, robot_states)