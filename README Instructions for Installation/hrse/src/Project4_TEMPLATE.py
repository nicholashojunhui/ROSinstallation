#!/usr/bin/env python

##### Workshop Day 4 - Interaction with Robots via Hand Gesture #####
##### to be inputed on ***right*** side of camera #####
##### to minimize background noise, setup a blue background #####

##### WITH Obstacle Avoidance Algorithm #####
##### Template Set; Look for "To be COMPLETED" #####

# Import relevant libraries
import cv2,time
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
import random
import numpy as np

# Open Camera
rospy.init_node('hand')
pub = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
m = Twist()
rate = rospy.Rate(60)
capture = cv2.VideoCapture(0)

scan0 = 0
scan45 = 0
scan90 = 0
scan135 = 0
scan180 = 0
scan225 = 0
scan270 = 0
scan315 = 0
allowance = 0.3

print('ONE : FORWARD')
print('TWO : COUNTERCLOCKWISE')
print('THREE : CLOCKWISE')
print('FOUR : REVERSE')

# function to collect laser scan data
#################### To be COMPLETED ####################

def callback(msg):
	global scan0, scan45, scan90, scan135, scan180, scan225, scan270, scan315
	#print('==== Laser Scan Details =====')
	#print('s1 [0]')
	#print msg.ranges[0]
	scan0 = msg.ranges[0]

	#print('s2 [45]')
	#print msg.ranges[45]
	scan45 = 

	#print('s3 [90]')
	#print msg.ranges[90]
	scan90 = 

	#print('s4 [135]')
	#print msg.ranges[135]
	scan135 = 

	#print('s5 [180]')
	#print msg.ranges[180]
	scan180 = 

	#print('s6 [225]')
	#print msg.ranges[225]
	scan225 = 

	#print('s7 [270]')
	#print msg.ranges[270]
	scan270 = 

	#print('s8 [315]')
	#print msg.ranges[315]
	scan315 = 

############################################################


# function to clear TB3 away from obstacles
#################### To be COMPLETED ####################

def clearance():

	if scan0 < allowance or scan45 < allowance or scan315 < allowance:
		m.linear.x = 

	elif scan180 < allowance or scan225 < allowance or scan135 < allowance:
		m.linear.x = 

	elif :
		m.angular.z = 
		m.linear.x = 

	elif :
		m.angular.z = 
		m.linear.x = 

	pub.publish(m)

############################################################

while(capture.isOpened()):
	
	# Capture frames from the camera
	ret, frame = capture.read()
	frame = cv2.flip(frame,1)
	
	# Get hand data from the rectangle sub window
	cv2.rectangle(frame, (450,80), (600,250), (0, 255, 0), 0)
	crop_image = frame[80:250,450:600]
	drawing = np.zeros(crop_image.shape,dtype =  np.uint8)

	# Apply Gaussian blur (also known as Gaussian smoothing); to reduce image noise and reduce detail
	blur = cv2.GaussianBlur(crop_image, (5, 5), 0)

	# Change color-space from BGR -> HSV
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	# Create a binary image with where white will be skin colors and rest is black
	mask2 = cv2.inRange(hsv, np.array([0, 20, 70]), np.array([20, 255, 255]))

	# Define Kernel (Filter Matrix or "Slider") for morphological transformation
	kernel = np.ones((5, 5))

############ Apply morphological transformations to filter out the background noise ##############
	# Filtering Sequence: Dilation, Erosion, Closing
	# Dilation is to gradually enlarge the boundaries of regions of foreground pixels, typically white pixels. As areas of foreground pixels grow in size, holes within those regions become smaller.
	# Erosion is to erode away the boundaries of regions of foreground pixels, typically white pixels. As areas of foreground pixels shrink in size, holes within those areas become larger.
	# Closing is simply as a dilation followed by an erosion using the same structuring element for both operations. The effect of this operator is to preserve background regions that have a similar shape to this structuring element, or that can completely contain the structuring element, while eliminating all other regions of background pixels.
##################################################################################################
	
	dilation = cv2.dilate(mask2, kernel, iterations=1)
	erosion = cv2.erode(dilation, kernel, iterations=1)
	closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, np.ones((5,5)))

	# Apply Gaussian Blur and Threshold (Otsu's thresholding after Gaussian filtering)
	# Thresholding is a technique in OpenCV, which is the assignment of pixel values in relation to the threshold value provided. In thresholding, each pixel value is compared with the threshold value. If the pixel value is smaller than the threshold, it is set to 0, otherwise, it is set to a maximum value (set to 255 in this case)
	filtered = cv2.GaussianBlur(erosion, (5, 5), 0)
	ret, thresh = cv2.threshold(filtered,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# Show threshold image
	cv2.imshow("Thresholded", thresh)
	# Find contours
	image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#_, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	try:
		# Find contour with maximum area
		contour = max(contours, key=lambda x: cv2.contourArea(x))

		# Create bounding rectangle around the contour
		x, y, w, h = cv2.boundingRect(contour)
		cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

		# Find convex hull; the set of pixels included in the smallest convex polygon that surround all input data.
		hull = cv2.convexHull(contour)


		# Draw contour; for our own visualization purposes
		drawing = np.zeros(crop_image.shape,dtype =  np.uint8)
		#drawing = np.zeros(crop_image.shape, np.uint8)
		cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
		cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

		# Find convexity defects; Any deviation of the object from the convex hull can be considered as convexity defect; 
		# returnPoints=True, then it returns the coordinates of the hull points. If returnPoints=False, it returns the indices of contour points corresponding to the hull points
		hull = cv2.convexHull(contour, returnPoints=False)

		# cv2.convexityDefects(contour, hull) returns an array where each row contains these values: [start point, end point, farthest point, approximate distance to farthest point]
		defects = cv2.convexityDefects(contour, hull)
		g = range(defects.shape[0])

		# Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger tips) for all defects
		count_defects = 0
		
		for i in g:
			s, e, f, d = defects[i, 0]
			start = tuple(contour[s][0])
			end = tuple(contour[e][0])
			far = tuple(contour[f][0])

			a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
			b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
			c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
			angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

			# if angle > 90 draw a circle at the far point
			if angle <= 90:
				count_defects += 1
				cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

			cv2.line(crop_image, start, end, [0, 255, 0], 2)
			#print ('count_defects:')
			#print (count_defects)


#################### To be COMPLETED ####################

		# TB3 Control Rules

		sub = rospy.Subscriber(, , )

		if scan0 < allowance or  <  or  <  or  <  or  <  or  <  or  <  or scan315 < allowance:
			m.linear.x = 
			m.angular.z = 
			print('braking due to obstacles detected')

			clearance()
			print('Clearing away from obstacles')

############################################################

		elif count_defects == 0:
			cv2.putText(frame, "ONE : FORWARD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
			m.linear.x = 0.2
			m.angular.z = 0
			print('forward')
		elif count_defects == 1:
			cv2.putText(frame, "TWO : COUNTERCLOCKWISE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
			m.linear.x = 0
			m.angular.z = 0.2
			print('left')
		elif count_defects == 2:
			cv2.putText(frame, "THREE : CLOCKWISE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
			m.linear.x = 0
			m.angular.z = -0.2
			print('right')
		elif count_defects == 3:
			cv2.putText(frame, "FOUR : REVERSE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
			m.angular.z = 0
			m.linear.x = -0.2
			print('reverse')
		elif count_defects == 4:
			cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		#else:
		#	m.linear.x = 0
		#	m.angular.z = 0
		#	print('braking')
			
		# Show required images
		pub.publish(m)
	except:
		# Brake if no gesture input
		m.linear.x = 0
		m.angular.z = 0
		print('braking due to no input')

		pub.publish(m)
		
		pass
	
	cv2.imshow("Gesture", frame)
	all_image = np.hstack((drawing, crop_image))
	cv2.imshow('Contours', all_image)
	if cv2.waitKey(3) == ord('q') or rospy.is_shutdown():
		print('Shutting Down!!!')
		break
	
capture.release()
