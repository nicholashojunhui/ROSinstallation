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
                            if not self.gridworld.is_wall(robot_x, robot_y):
                                state = (robot_x, robot_y, human_x, human_y, human_request)   # this is a 5-tuple
                                states.add(state)

#################### assign reward[state] here below #################### 
	
                                # Start codes here




#########################################################################

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

######### return a list of 2-tuples (i.e. complete this section) #########

            return [(0.5, self.execute_one_step(state, action, 'S')),
                    ]

##########################################################################

        else:
            return [(0.0, state)]

    def T(self, state, action):
        #print(self.transitions[state][action])
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

######## implement this function based on robot_execute_one_step ########

	# Start codes here
        current_cell = 			# Current Human Position States
        current_action = 		# Current Human Action
        next_cell = 			# Next Cell Position
        
        if 				# Toggle Request from Human and current status is 'False'
        elif 				# Toggle Request from Human and current status is 'True'
            next_state = [next_cell, 0]
        else:				# NO Toggle Request from Human
            next_state = [next_cell, state[4]]
        #print(next_state)

        if  				# Check if human is hitting wall
            return XXXX
        else:
            return( XXXX, XXXX, next_cell[0], next_cell[1], XXXX)

##########################################################################

    def execute_one_step(self, state, robot_action, human_action):
        return self.human_execute_one_step(self.robot_execute_one_step(state, robot_action), human_action)


# example runs if you get it right
gridworld = load_gridworld('world1.csv')
hrimdp = HRIMDP(gridworld, terminals=[])

U = value_iteration(hrimdp)

print("================")
for row in range(gridworld.num_row):
    for col in range(gridworld.num_col):
        if (row, col, 2,3,1) in U:
            print(U[(row, col, 2,3,1)],'\t', end='')
        else:
            print('None','\t', end='')
    print()

''' expected output values
20.767288525647075 	25.375885938575383 	30.821529263678997 	36.39181265275612 	
23.32543276373877 	None 	36.417692725138345 	48.179152814054575 	
29.174435465501716 	36.417692725138345 	48.179152814054575 	48.179152814054575
'''

print("================")
for row in range(gridworld.num_row):
    for col in range(gridworld.num_col):
        if (row, col, 0,0,0) in U:
            print(U[(row, col, 0,0,0)],'\t', end='')
        else:
            print('None','\t', end='')
    print()

''' expected output values
-9.478256397118312 	-5.042542092748368 	2.473747207906275 	6.473747207906275 	
-5.442807035314319 	None 	6.296524215658065 	6.473747207906275 	
1.8649942492409748 	6.068869318410732 	6.068869318410732 	6.296524215658065  
'''


