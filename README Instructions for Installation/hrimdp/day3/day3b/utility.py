import sys
import csv
import time

from gridworld import GridWorld

def load_gridworld(filename):
	grid = []
	with open(filename, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			grid_row = []
			for col in row:
				grid_row.append(int(col))
			grid.append(grid_row)
	return GridWorld(grid)

def load_actions(filename):
	with open(filename, newline='') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			return row

def load_human_states(filename):
	states = []
	with open(filename, newline='') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			states.append([[int(row[0]), int(row[1])], int(row[2])])
	return states

def load_robot_states(filename):
	states = []
	with open(filename, newline='') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			states.append([int(row[0]), int(row[1])])
	return states

def record_human_states(filename, states):
	with open(filename, 'w', newline='') as f:
		writer = csv.writer(f)
		for state in states:
			writer.writerow([state[0][0], state[0][1], state[1]])

def record_robot_states(filename, robot_states):
	with open(filename, 'w', newline='') as f:
		writer = csv.writer(f, delimiter=',')
		for state in robot_states:
			writer.writerow([state[0], state[1]])

def record_human_actions(filename, actions):
	with open(filename, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(actions)
