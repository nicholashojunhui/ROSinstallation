import sys

from utility import *
from gridworld import GridWorld

from rewards import *

def visualize(gridworld, timestamps, human_trajectory=None, robot_trajectory=None, rewards_trajectory=None):
	gridworld.reset()
	gridworld.show()
	time.sleep(1)

	for t in range(timestamps):
		# reset background
		gridworld.reset()

		# draw reward
		if rewards_trajectory is not None:
			rewards = rewards_trajectory[t]
			gridworld.draw_rewards(rewards)

		# draw human and robot
		if human_trajectory is not None:
			#print(f'Human traj = {human_trajectory[t][0]}, toggle = {human_trajectory[t][1]}')
			gridworld.draw_human(human_trajectory[t][0])

		if robot_trajectory is not None:
			# print(f'Robot traj = {robot_trajectory[t]}')
			gridworld.draw_robot(robot_trajectory[t])
	
		# show and sleep
		gridworld.show(str(t))
		time.sleep(0.5)
		
	gridworld.loop()

if len(sys.argv) != 4:
	print()
	print("usage: python3 visualizer.py gridworld.csv human_states.csv robot_states.csv")
	exit()

gridworld_filename = sys.argv[1]
human_states_filename = sys.argv[2]
robot_states_filename = sys.argv[3]

gridworld = load_gridworld(gridworld_filename)
human_states = load_human_states(human_states_filename)
robot_states = load_robot_states(robot_states_filename)

rewards_trajectory = compute_rewards_trajectory(gridworld, human_states)

visualize(gridworld, min(len(robot_states), len(human_states)), human_trajectory=human_states, robot_trajectory=robot_states, rewards_trajectory=rewards_trajectory)
