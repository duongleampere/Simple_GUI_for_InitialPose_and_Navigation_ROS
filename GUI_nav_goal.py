#!/usr/bin/env python

import tkinter as tk
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback, MoveBaseResult
import tf

rospy.init_node('send_client_goal')

client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
Init = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)

rospy.loginfo("Waiting for move base server")
client.wait_for_server()

goal = MoveBaseGoal()
start_pos = PoseWithCovarianceStamped()

root= tk.Tk()
#///////////////////////Nav_goal/////////////////////////
canvas_nav_1 = tk.Canvas(root, width = 450, height = 300)
canvas_nav_1.pack()

entry_nav_1 = tk.Entry (root) 
canvas_nav_1.create_window(120, 40, window=entry_nav_1)

entry_nav_2 = tk.Entry (root) 
canvas_nav_1.create_window(120, 60, window=entry_nav_2)

entry_nav_3 = tk.Entry (root) 
canvas_nav_1.create_window(120, 80, window=entry_nav_3)

label_nav_1 = tk.Label(root, text= 'x')
canvas_nav_1.create_window(20, 40, window=label_nav_1)

label_nav_2 = tk.Label(root, text= 'y')
canvas_nav_1.create_window(20, 60, window=label_nav_2)

label_nav_3 = tk.Label(root, text= 'theta')
canvas_nav_1.create_window(20, 80, window=label_nav_3)

#///////////////////////InitialPose/////////////////////////
entry_init_1 = tk.Entry (root) 
canvas_nav_1.create_window(320, 40, window=entry_init_1)

entry_init_2 = tk.Entry (root) 
canvas_nav_1.create_window(320, 60, window=entry_init_2)

entry_init_3 = tk.Entry (root) 
canvas_nav_1.create_window(320, 80, window=entry_init_3)

label_init_1 = tk.Label(root, text= 'x')
canvas_nav_1.create_window(220, 40, window=label_init_1)

label_init_2 = tk.Label(root, text= 'y')
canvas_nav_1.create_window(220, 60, window=label_init_2)

label_init_3 = tk.Label(root, text= 'theta')
canvas_nav_1.create_window(220, 80, window=label_init_3)


def nav_goal():  
    x1 = entry_nav_1.get()
    y1 = entry_nav_2.get()
    theta1 = entry_nav_3.get()
    odom_quat1 = tf.transformations.quaternion_from_euler(0, 0, theta1)

    goal.target_pose.header.frame_id = 'map' 
    goal.target_pose.pose.position.x = float(x1)
    goal.target_pose.pose.position.y = float(y1)
    goal.target_pose.pose.orientation.z = float(odom_quat1[2])
    goal.target_pose.pose.orientation.w = float(odom_quat1[3])
	
    client.send_goal(goal)
    client.wait_for_result()
    #label1 = tk.Label(root, text= float(x1)**0.5)
    #canvas1.create_window(200, 230, window=label1)

def InitialPose():  
    x1 = entry_init_1.get()
    y1 = entry_init_2.get()
    theta1 = entry_init_3.get()
    odom_quat1 = tf.transformations.quaternion_from_euler(0, 0, theta1)

    start_pos.header.frame_id = 'map' 
    start_pos.header.stamp = rospy.Time.now()
    start_pos.pose.pose.position.x = float(x1)
    start_pos.pose.pose.position.y = float(y1)
    start_pos.pose.pose.position.z = 0.0

    start_pos.pose.pose.orientation.x  = float(odom_quat1[0])
    start_pos.pose.pose.orientation.y = float(odom_quat1[1])
    start_pos.pose.pose.orientation.z = float(odom_quat1[2])
    start_pos.pose.pose.orientation.w = float(odom_quat1[3])
	
    rospy.loginfo(start_pos)
    Init.publish(start_pos)
    #label1 = tk.Label(root, text= float(x1)**0.5)
    #canvas1.create_window(200, 230, window=label1)
    
button_nav_1 = tk.Button(text='MoveBaseGoal', command=nav_goal)
canvas_nav_1.create_window(90, 130, window=button_nav_1)

button_init_1 = tk.Button(text='InitialPose', command=InitialPose)
canvas_nav_1.create_window(290, 130, window=button_init_1)

root.mainloop()