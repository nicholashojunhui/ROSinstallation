import sys

from utility import *
from gridworld import GridWorld

from hrimdp import *

robot_actions = {'L': [0,-1], 'R': [0,1], 'U': [-1,0], 'D': [1,0], 'S': [0,0]}

def robot_execute_under_policy(gridworld, robot_init_state, policy, human_states):
	robot_states = []

	# to be filled

	rs = robot_init_state
	for hs in human_states:
		query = (rs[0], rs[1], hs[0][0], hs[0][1], hs[1])
		# if query in policy:
		# 	current_policy = policy[query]
		# else:
		# 	current_policy = 'S'
		try:
			current_policy = policy[query]
		except Exception as e:
			#print(f'****** ERROR: {e}')
			print("****** ERROR: {e}")
		
		current_action = robot_actions[current_policy]
		next_cell = [c + a for c, a in zip(rs, current_action)]

		if gridworld.is_wall(next_cell[0], next_cell[1]):
			robot_states.append((rs[0], rs[1]))
		else:
			rs = next_cell
			robot_states.append(rs)

	# return robot_states
	return robot_states

if len(sys.argv) != 6:
	print()
	print("usage: python3 planner.py gridworld.csv human_state.csv robot_x robot_y output_robot_states.csv")
	exit()

gridworld_filename = sys.argv[1]
human_states_filename = sys.argv[2]
robot_init_x = int(sys.argv[3])
robot_init_y = int(sys.argv[4])
robot_states_filename = sys.argv[5]

gridworld = load_gridworld(gridworld_filename)
human_states = load_human_states(human_states_filename)

hrimdp = HRIMDP(gridworld, terminals=[])
U = value_iteration(hrimdp)
policy = best_policy(hrimdp, U)
robot_states = robot_execute_under_policy(gridworld, [robot_init_x, robot_init_y], policy, human_states)

record_robot_states(robot_states_filename, robot_states)
