#!/usr/bin/env python

######## DEMO No. 1 for HRSE (TB3) ########
######## Uploading data to ThingSpeak Platform while autonomously exploring map ########

# Import necessary packages needed to send data
from __future__ import print_function
import paho.mqtt.publish as publish
import psutil
from time import sleep
from math import isnan

# Import necessary packages for TB3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

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


#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = True

# Set useSecuredTCP to True to use the default MQTT port of 8883
# This type of unsecured MQTT connection uses the least amount of system resources.
useSecuredTCP = False

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = False

#####   End of user configuration   #####

# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
	tTransport = "tcp"
	tPort = 1883
	tTLS = None

if useSecuredTCP:
	tTransport = "tcp"
	tPort = 8883
	tTLS = None

if useUnsecuredWebsockets:
	tTransport = "websockets"
	tPort = 80
	tTLS = None

if useSSLWebsockets:
	import ssl
	tTransport = "websockets"
	tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
	tPort = 443

# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey


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

rospy.init_node('obstacle_avoidance')	# Initiate a Node called 'obstacle_avoidance'


while not rospy.is_shutdown():

	pub = rospy.Publisher('/cmd_vel', Twist)
	move = Twist()

	sub = rospy.Subscriber('/scan', LaserScan, callback)

	##### Send laserdata to ThingSpeak #####

	# build the payload string
	tPayload = "field1=" + str(data1) + "&field2=" + str(data2) + "&field3=" + str(data3) + "&field4=" + str(data4) + "&field5=" + str(data5) + "&field6=" + str(data6)


	# attempt to publish this data to the topic 
	publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

	###################################

	# Obstacle Avoidance Simple Algo:

	if data1 >= 0.5 and data2 >= 0.5 and data6 >= 0.5:
		move.linear.x = 0.4
		move.angular.z = 0.0
	elif data2 < 0.5:
		move.linear.x = 0.0
		move.angular.z = -1	#60 degrees to right
	elif data6 < 0.5:
		move.linear.x = 0.0
		move.angular.z = 1	#60 degrees to left
	else:
		move.linear.x = 0.0
		move.angular.z = 1.57	#90 degrees to left

	pub.publish(move)
	
	

rospy.spin()


