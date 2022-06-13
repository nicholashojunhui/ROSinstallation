from utils import print_table
from mdp import *

sequential_decision_environment_without_terminal_1 = GridMDP([[-0.04, -0.04, -0.04, +1],
                                                	       [-0.04, None, -0.04, -1],
                                                	       [-0.04, -0.04, -0.04, -0.04]],
                                                		terminals=[])

sequential_decision_environment_without_terminal_2 = GridMDP([[-0.04, -0.04, -0.04, +1],
                                                                [-0.04, None, -0.04, -100],
                                                		[-0.04, -0.04, -0.04, -0.04]],
                                                		terminals=[])


def visualize_best_policy(mdp):
	pi = best_policy(mdp, value_iteration(mdp))
	print ("=== best_policy ===")
	print_table(mdp.to_arrows(pi))
	print ("===================")


visualize_best_policy(sequential_decision_environment_without_terminal_1)
visualize_best_policy(sequential_decision_environment_without_terminal_2)