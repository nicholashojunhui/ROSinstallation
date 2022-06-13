from gridworld import GridWorld

def compute_rewards(gridworld, human_state):
	num_col = gridworld.num_col
	num_row = gridworld.num_row

	rewards = [[-1 for col in range(num_col)] for row in range(num_row)]
	
	# to be filled

	hs_x = human_state[0][0]
	hs_y = human_state[0][1]
	# print(f'rg = {rewards_grid}')
	# print(f'x = {hs_x}, y = {hs_y}')
	if human_state[1] == 0:
		if not gridworld.is_wall(hs_x, hs_y): rewards[hs_x][hs_y] = -10
		if not gridworld.is_wall(hs_x-1, hs_y): rewards[hs_x-1][hs_y] = -10
		if not gridworld.is_wall(hs_x+1, hs_y): rewards[hs_x+1][hs_y] = -10
		if not gridworld.is_wall(hs_x, hs_y-1): rewards[hs_x][hs_y-1] = -10
		if not gridworld.is_wall(hs_x, hs_y+1): rewards[hs_x][hs_y+1] = -10

		if not gridworld.is_wall(hs_x-2, hs_y): rewards[hs_x-2][hs_y] = -5
		if not gridworld.is_wall(hs_x+2, hs_y): rewards[hs_x+2][hs_y] = -5
		if not gridworld.is_wall(hs_x, hs_y-2): rewards[hs_x][hs_y-2] = -5
		if not gridworld.is_wall(hs_x, hs_y+2): rewards[hs_x][hs_y+2] = -5

		if not gridworld.is_wall(hs_x-1, hs_y-1): rewards[hs_x-1][hs_y-1] = -5
		if not gridworld.is_wall(hs_x-1, hs_y+1): rewards[hs_x-1][hs_y+1] = -5
		if not gridworld.is_wall(hs_x+1, hs_y+1): rewards[hs_x+1][hs_y+1] = -5
		if not gridworld.is_wall(hs_x+1, hs_y-1): rewards[hs_x+1][hs_y-1] = -5

	if human_state[1] == 1:
		if not gridworld.is_wall(hs_x, hs_y): rewards[hs_x][hs_y] = 10
		if not gridworld.is_wall(hs_x-1, hs_y): rewards[hs_x-1][hs_y] = 10
		if not gridworld.is_wall(hs_x+1, hs_y): rewards[hs_x+1][hs_y] = 10
		if not gridworld.is_wall(hs_x, hs_y-1): rewards[hs_x][hs_y-1] = 10
		if not gridworld.is_wall(hs_x, hs_y+1): rewards[hs_x][hs_y+1] = 10
	return rewards

def compute_rewards_trajectory(gridworld, human_trajectory):
	rewards_trajectory = []
	for state in human_trajectory:
		rewards_trajectory.append(compute_rewards(gridworld, state))
	return rewards_trajectory


