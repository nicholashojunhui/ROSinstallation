from mdp import *
from utility import load_gridworld

robot_actions = {'L': [0,-1], 'R': [0,1], 'U': [-1,0], 'D': [1,0], 'S': [0,0]}
human_actions = {'L': [0,-1], 'R': [0,1], 'U': [-1,0], 'D': [1,0], 'S': [0,0], 'T': [0,0]}

class HRIMDP(MDP):
    """A 5-dimensional gridworld MDP. 
    specify the gridworld object, 0 for free space, 1 for obstacle
    Action space contains all robot actions.
    Uncertainty is due to uncertain human actions."""

    def __init__(self, gridworld, terminals, init=(0, 0, 0, 0, 0), gamma=.9):
        reward = {}
        states = set()
        self.rows = gridworld.num_row
        self.cols = gridworld.num_col
        self.gridworld = gridworld        # instead of a 2-d array of rewards. this is our gridworld object

        # 5-dimensional grid MDP
        for robot_x in range(self.rows):
            for robot_y in range(self.cols):
                for human_x in range(self.rows):
                    for human_y in range(self.cols):
                        for human_request in (0,1):
                            if not self.gridworld.is_wall(robot_x, robot_y) and not self.gridworld.is_wall(human_x, human_y):
                                state = (robot_x, robot_y, human_x, human_y, human_request)   # this is a 5-tuple
                                states.add(state)

                                # assign reward[state] here
                                human_state = [[human_x, human_y], human_request]
                                reward_grid = compute_rewards(gridworld, human_state)
                                reward[state] = reward_grid[robot_x][robot_y]
        self.states = states

        actlist = list(robot_actions.keys())
        transitions = {}
        for s in states:
            transitions[s] = {}
            for a in actlist:
                transitions[s][a] = self.calculate_T(s, a)
        MDP.__init__(self, init, actlist=actlist,
                     terminals=terminals, transitions=transitions,
                     reward=reward, states=states, gamma=gamma)

    def calculate_T(self, state, action):
        if action:
            # return a list of 2-tuples instead of None
            return [(0.5, self.execute_one_step(state, action, 'S')),
                    (0.1, self.execute_one_step(state, action, 'L')),
                    (0.1, self.execute_one_step(state, action, 'R')),
                    (0.1, self.execute_one_step(state, action, 'U')),
                    (0.1, self.execute_one_step(state, action, 'D')),
                    (0.1, self.execute_one_step(state, action, 'T'))]
        else:
            return [(0.0, state)]

    def T(self, state, action):
        return self.transitions[state][action] if action else [(0.0, state)]

    def robot_execute_one_step(self, state, action):
        current_cell = [state[0], state[1]]
        current_action = robot_actions[action]
        next_cell = [c + a for c, a in zip(current_cell, current_action)]
        
        if self.gridworld.is_wall(next_cell[0], next_cell[1]):
            return state
        else:
            return (next_cell[0], next_cell[1], state[2], state[3], state[4])

    def human_execute_one_step(self, state, action):
        # implement this function based on robot_execute_one_step
        current_cell = [state[2], state[3]]
        current_action = human_actions[action]
        next_cell = [c + a for c, a in zip(current_cell, current_action)]
        togglestate = state[4]
        if action == 'T':
            togglestate = 1 - togglestate    

        if self.gridworld.is_wall(next_cell[0], next_cell[1]):
            # return (state[2], state[3])
            return state
        else:
            return (state[0], state[1], next_cell[0], next_cell[1], togglestate)


    def execute_one_step(self, state, robot_action, human_action):
        return self.human_execute_one_step(self.robot_execute_one_step(state, robot_action), human_action)

def compute_rewards(gridworld, human_state):
	# implement this funciton
	gc = gridworld.num_col
	gr = gridworld.num_row

	rewards_grid = [[-1 for col in range(gc)] for row in range(gr)]
	hs_x = human_state[0][0]
	hs_y = human_state[0][1]
	#print(f'rg = {rewards_grid}') #for python3.6
	#print(f'x = {hs_x}, y = {hs_y}') #for python3.6

	print("rg = {}".format(rewards_grid))
	print("x =  {}".format(hs_x), "y =  {}".format(hs_y))

	if human_state[1] == 0:
		if not gridworld.is_wall(hs_x, hs_y): rewards_grid[hs_x][hs_y] = -10
		if not gridworld.is_wall(hs_x-1, hs_y): rewards_grid[hs_x-1][hs_y] = -10
		if not gridworld.is_wall(hs_x+1, hs_y): rewards_grid[hs_x+1][hs_y] = -10
		if not gridworld.is_wall(hs_x, hs_y-1): rewards_grid[hs_x][hs_y-1] = -10
		if not gridworld.is_wall(hs_x, hs_y+1): rewards_grid[hs_x][hs_y+1] = -10

		if not gridworld.is_wall(hs_x-2, hs_y): rewards_grid[hs_x-2][hs_y] = -5
		if not gridworld.is_wall(hs_x+2, hs_y): rewards_grid[hs_x+2][hs_y] = -5
		if not gridworld.is_wall(hs_x, hs_y-2): rewards_grid[hs_x][hs_y-2] = -5
		if not gridworld.is_wall(hs_x, hs_y+2): rewards_grid[hs_x][hs_y+2] = -5

		if not gridworld.is_wall(hs_x-1, hs_y-1): rewards_grid[hs_x-1][hs_y-1] = -5
		if not gridworld.is_wall(hs_x-1, hs_y+1): rewards_grid[hs_x-1][hs_y+1] = -5
		if not gridworld.is_wall(hs_x+1, hs_y+1): rewards_grid[hs_x+1][hs_y+1] = -5
		if not gridworld.is_wall(hs_x+1, hs_y-1): rewards_grid[hs_x+1][hs_y-1] = -5

	if human_state[1] == 1:
		if not gridworld.is_wall(hs_x, hs_y): rewards_grid[hs_x][hs_y] = 10
		if not gridworld.is_wall(hs_x-1, hs_y): rewards_grid[hs_x-1][hs_y] = 10
		if not gridworld.is_wall(hs_x+1, hs_y): rewards_grid[hs_x+1][hs_y] = 10
		if not gridworld.is_wall(hs_x, hs_y-1): rewards_grid[hs_x][hs_y-1] = 10
		if not gridworld.is_wall(hs_x, hs_y+1): rewards_grid[hs_x][hs_y+1] = 10

	return rewards_grid
