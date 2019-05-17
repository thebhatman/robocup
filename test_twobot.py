import rospy,sys
from utils.geometry import Vector2D
from utils.functions import *
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import BeliefState
from multiprocessing import Process
from kubs import kubs
from krssg_ssl_msgs.srv import bsServer
from math import atan2,pi
from utils.functions import *
from role import two_bot

from tactics import  sample_tactic, CoPass

pub = rospy.Publisher('/grsim_data',gr_Commands,queue_size=1000)


def function(id_,state):
	bot_1 = kubs.kubs(0,state,pub)
	bot_1.update_state(state)
	bot_2 = kubs.kubs(1,state,pub)
	bot_2.update_state(state)
	pr_fsm = two_bot.TwoBot()
	pr_fsm.add_kub(bot_1)
	pr_fsm.add_kub(bot_2)
	pr_fsm.as_graphviz()
	pr_fsm.write_diagram_png()
	pr_fsm.spin_cb()
	# # global flag
	# 
# 	kub = kubs.kubs(id_,state,pub)
# 	# print(kub.kubs_id)
# 	g_fsm = sample_tactic.SampleTactic()
# 	# print(kub.kubs_id+1)
# 	g_fsm.add_kub(kub)
	# print(kub.kubs_id+2)

	# g_fsm.as_graphviz()
	# g_fsm.write_diagram_png()
	# g_fsm.spin_cb()
	# # print(kub.kubs_id+3)
rospy.init_node('node_new',anonymous=False)
start_time = rospy.Time.now()

start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)   



while True:
	state = None
	rospy.wait_for_service('bsServer',)
	getState = rospy.ServiceProxy('bsServer',bsServer)
	try:
		state = getState(state)
	except rospy.ServiceException, e:
		print e	
	if state:
		function(1,state.stateB)
rospy.spin()