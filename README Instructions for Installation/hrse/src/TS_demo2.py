#!/usr/bin/env python

######## DEMO No. 2 for HRSE (TB3) ########
######## Uploading data to ThingSpeak Platform while manual driving ########

# Import necessary packages needed to send data
from __future__ import print_function
import paho.mqtt.publish as publish
import psutil
import thingspeak
from time import sleep
from math import isnan

# Import necessary packages for TB3
import rospy
from sensor_msgs.msg import LaserScan

# defining field variables (to send to ThingSpeak)
data1 = 0
data2 = 0
data3 = 0
data4 = 0
data5 = 0
data6 = 0

#####  ThingSpeak Channel Settings #####

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "1111205"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "XXXXXXXXXXXXXXXXXXXXX"

channel = thingspeak.Channel(id=channelID, api_key=apiKey)

#####   End of user configuration   #####


###### Start of functions ######

def callback(msg):
	print('=========================================')
	print('s1 [0]')
	print (msg.ranges[0])

	print('s2 [45]')
	print (msg.ranges[45])

	print('s3 [90]')
	print (msg.ranges[90])

	print('s4 [180]')
	print (msg.ranges[180])

	print('s5 [270]')
	print (msg.ranges[270])

	print('s6 [315]')
	print (msg.ranges[315])

	# assigning values to global variables
	global data1, data2, data3, data4, data5, data6
	data1 = msg.ranges[0]
	data2 = msg.ranges[45]
	data3 = msg.ranges[90]
	data4 = msg.ranges[180]
	data5 = msg.ranges[270]
	data6 = msg.ranges[315]


rospy.init_node('laser_scan')			# Initiate a Node called 'laser_scan'


while not rospy.is_shutdown():
	
	sub = rospy.Subscriber('/scan', LaserScan, callback)

	##### Send laserdata to ThingSpeak #####

	channel.update({'field1': str(data1), 'field2': str(data2), 'field3': str(data3), 'field4': str(data4), 'field5': str(data5), 'field6': str(data6)})

	###################################



rospy.spin()


