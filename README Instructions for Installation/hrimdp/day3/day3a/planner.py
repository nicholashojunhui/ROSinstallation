import sys

from utility import *
from gridworld import GridWorld

from hrimdp import *

robot_actions = {'L': [0,-1], 'R': [0,1], 'U': [-1,0], 'D': [1,0], 'S': [0,0]}

def robot_execute_under_policy(gridworld, robot_init_state, policy, human_states):
	robot_states = []
############## to be completed here; XXXX are parts to be edited ##############
	# print(f "policy {policy[(2, 0, 0, 1, 1)]}") #for python3.6
	# print("policy {}".format(policy[(2, 0, 0, 1, 1)]))

	rs = robot_init_state

	for hs in human_states:
		query = (XXXX, XXXX, XXXX, XXXX, XXXX) #include the robot position states, human position states, followed by human request status; refer to hrimdp.py for clues

		#print(f'query = {query}') #for python3.6
		print("query = {}".format(query))

		current_policy = policy[XXXX] 		# update policy
		current_action = robot_actions[XXXX]	# update robot actions
		next_cell = [c + a for c, a in zip(XXXX, XXXX)] # update robot position states

		if gridworld.is_wall(next_cell[0], next_cell[1]):	# robot is hitting wall
			robot_states.append((XXXX, XXXX))	#state remains the same
		else:						# robot is not hitting wall
			rs = next_cell		# Update rs variable with new values
			robot_states.append(rs) # Update robot position states with new values

######################################################################

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
