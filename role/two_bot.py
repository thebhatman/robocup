from enum import Enum
import composite_behavior
import behavior
import GoToPoint
import rospy
from utils.functions import *
from utils.config import *
from utils.geometry import Vector2D

class TwoBot(composite_behavior.CompositeBehavior):
    """docstring for GoToPoint"""
    ##
    ## @brief      Class for state.
    ##
    class State(Enum):
        setup = 1 
        drive = 2


    def __init__(self,continuous=False):
        # print "gtp"
        #GoToPoint.behavior.Behavior()
        #g = behavior.Behavior()
        #print "gtp2"
        super(TwoBot,self).__init__()
        #self.state = state

        self.name = "TwoBot"
        self.kub = []

        self.behavior_failed = False
        self.DISTANCE_THRESH = DISTANCE_THRESH

        self.add_state(TwoBot.State.setup,
            behavior.Behavior.State.running)
        self.add_state(TwoBot.State.drive,
            behavior.Behavior.State.running)
        

        self.add_transition(behavior.Behavior.State.start,
            TwoBot.State.setup,lambda: True,'immediately')

        self.add_transition(TwoBot.State.setup,
            TwoBot.State.drive,lambda:self.target_present(),'setup')

        #self.add_transition(TwoBot.State.drive,
        #    TwoBot.State.drive,lambda: not self.at_new_point(),'restart')

        self.add_transition(TwoBot.State.drive,
            behavior.Behavior.State.completed,lambda:self.subbehavior_with_name('move bot 0').state == behavior.Behavior.State.completed
            and self.subbehavior_with_name('move bot 1').state == behavior.Behavior.State.completed,'complete')

        self.add_transition(TwoBot.State.setup,
            behavior.Behavior.State.failed,lambda: self.subbehavior_with_name('move bot 0').state == behavior.Behavior.State.failed
            or self.subbehavior_with_name('move bot 1').state == behavior.Behavior.State.failed,'failed')

        self.add_transition(TwoBot.State.drive,
            behavior.Behavior.State.failed,lambda: self.subbehavior_with_name('move bot 0').state == behavior.Behavior.State.failed
            or self.subbehavior_with_name('move bot 1').state == behavior.Behavior.State.failed,'failed')

        self.add_transition(behavior.Behavior.State.completed,
            TwoBot.State.setup,lambda: self.all_subbehaviors_completed(),'oscillation')


    def target_point(self,kub):
        target = Vector2D()
        if(kub.kubs_id == self.kub[0].kubs_id):
            if(kub.state.homePos[kub.kubs_id].y > 0):
                target.x = 2000
                target.y = -2000
            else:
                target.x = 2000
                target.y = 2000
            self.target_points += [target]
        else:
            if(kub.state.homePos[kub.kubs_id].y > 0):
                target.x = -2000
                target.y = -2000
            else:
                target.x = -2000
                target.y = 2000
            self.target_points += [target]
        
    def add_kub(self,kub):
        self.kub += [kub]
        
    def target_present(self):
        return len(self.target_points) == 2 


    def at_new_point(self):
        #print (dist(self.target_point,self.new_point),210)
        return dist(self.target_point,self.new_point) < self.DISTANCE_THRESH

        
    def on_enter_setup(self):
        self.move = []
        self.target_points = []
        self.remove_all_subbehaviors()
        pass
    def execute_setup(self):
        self.move += [GoToPoint.GoToPoint()]
        self.move[0].add_kub(self.kub[0])
        self.target_point(self.kub[0])
        self.add_subbehavior(self.move[0], 'move bot 0')
        self.move += [GoToPoint.GoToPoint()]
        self.move[1].add_kub(self.kub[1])
        self.target_point(self.kub[1])
        self.add_subbehavior(self.move[1], 'move bot 1')
        pass
        
    def on_exit_setup(self):
        pass

    def on_enter_drive(self):
        self.move[0].add_point(self.target_points[0])
        self.move[1].add_point(self.target_points[1])
        pass

    def terminate(self):
        super().terminate()

    def execute_drive(self):
        print("Execute drive")
        # start_time = rospy.Time.now()
        # start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
        # _GoToPoint_.init(self.kub,self.target_point,self.theta)
        # generatingfunction = _GoToPoint_.execute(start_time,self.DISTANCE_THRESH)
        # print("Datatype of gf:",type(generatingfunction))
        # for gf in generatingfunction:
        #     self.kub,target_point = gf

        #     # print self.behavior_failed
        #     if not vicinity_points(self.target_point,target_point):
        #         # print 
        #         # print  (self.target_point.x,self.target_point.y)
        #         # print  (target_point.x,target_point.y)
        #         # print 
        #         self.behavior_failed = True
        #         # print self.behavior_failed
        #         break    
    def on_exit_drive(self):
        pass




