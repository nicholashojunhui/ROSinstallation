from gridworld import GridWorld

def compute_rewards(gridworld, human_state):
	
	num_col = gridworld.num_col
	num_row = gridworld.num_row

	rewards = [[-1 for col in range(num_col)] for row in range(num_row)]
	
	# to be filled
	cell = human_state[0]
	is_positive = human_state[1]
	for row in range(num_row):
		for col in range(num_col):
			if gridworld.is_wall(row, col):
				rewards[row][col] = None

			if (abs(row - cell[0]) + abs(col - cell[1])) <= 1:
				rewards[row][col] = (10 if is_positive else -10)

			if 1 < (abs(row - cell[0]) + abs(col - cell[1])) <= 2 and not is_positive:
				rewards[row][col] = -5

	return rewards


def compute_rewards_trajectory(gridworld, human_trajectory):
	rewards_trajectory = []
	for state in human_trajectory:
		rewards_trajectory.append(compute_rewards(gridworld, state))
	return rewards_trajectory


