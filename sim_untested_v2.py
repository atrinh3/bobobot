from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.lines as lin
from time import time
import numpy as np
import math

DEBUG = True

class Bobo:
    def __init__(self, arms):
        self.arm1 = arms[0]
        self.arm2 = arms[1]
        self.angle1 = arm1.angle
        self.angle2 = arm2.angle
        self.w1 = 0
        self.w2 = 0
        self.time_elapsed = 0
        self.target = self.arm2.get_endpoint()
        self.moving = False
        self.torque = .25  # 1 deg / sec

    def position(self):
        return self.arm2.get_endpoint()

    def get_x(self):
        x = [self.arm1.origin[0], self.arm2.origin[0], self.position()[0]]
        return x

    def get_y(self):
        y = [self.arm1.origin[1], self.arm2.origin[1], self.position()[1]]
        return y

    def reach(self, new_target, dt):
        print("Reaching for target")
        # if "under the table" may have to move arm1 back to
        # retract arm2 first before moving above the table

        # angle to target
        self.target = new_target
        self.moving = True
        self.step(dt)

    def reset(self, dt):
        print("Resetting arms :)")
        self.reach([10, -10], dt)

    def distance(self, coordinate):
        return math.hypot(coordinate[0], coordinate[1])
    
    def angle(self, coordinate):
        return math.degrees(math.atan(coordinate[1] / coordinate[0]))

    def move_arm1(self, distance):
        self.arm1.move(distance)
        self.arm2.set_origin(self.arm1.get_endpoint())

    def move_arm2(self, distance):
        if self.target_prox() > .5:
            self.arm2.move(distance)
        else:
            self.moving = False
            if DEBUG:
                print("self.moving = False")

    def a1_target(self, target):
        # There should almost always be 2 points where the arm is in range
        # Pick the one that has the lower value.
        d_target = self.distance(target)
        a_target = self.angle(target)
        return a_target - math.degrees(math.cos((d_target/2)/self.arm2.length))
        
        
        
    def step(self, dt):
        if self.moving:
            # find direction to move arm1
            a1_aim = self.a1_target(self.target)
            print(a1_aim)
            # find new angle for arm 2 resulting from arm1 movement
            a2_target = math.degrees(math.atan((self.target[1] - self.position()[1]) /
                                               (self.target[0] - self.position()[0])))
            if DEBUG:
                #print("{time} - Current Position: {pos}, target prox: {prox}".format(
                #    time=self.time_elapsed, pos=self.position(), prox=self.target_prox()))
            
            while self.moving:
                # adjust arm1 by some degrees
                self.move_arm1(np.sign(a1_limit - self.arm1.angle) * self.torque * dt)

                # adjust arm2 by some degrees
                self.move_arm2(np.sign(a2_target - self.arm2.angle) * self.torque * dt)
                self.time_elapsed += dt
                if DEBUG:
                    #print("{time} - Current Position: {pos}, target prox: {prox}".format(
                    #    time=self.time_elapsed, pos=self.position(), prox=self.target_prox()))
            print("Done reaching")


class Arm:
    def __init__(self, arm_length, arm_origin, arm_angle):
        self.length = arm_length
        self.origin = arm_origin
        self.angle = arm_angle

    def move(self, distance):
        self.angle += distance

    def set_origin(self, origin):
        self.origin = origin

    def get_endpoint(self):
        # x_end
        x = self.origin[0] + (self.length * math.cos(math.radians(self.angle)))

        # y_end
        y = self.origin[1] + (self.length * math.sin(math.radians(self.angle)))

        endpoint = [round(x, 3), round(y, 3)]
        return endpoint
        
arm1 = Arm(10, [0, 0], -90)
arm2 = Arm(10, arm1.get_endpoint(), 0)
arms = [arm1, arm2]
rob = Bobo(arms)

dt = 1 

#fig = plt.figure()
#ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 25), ylim=(-20, 10))

# for i in range(0, len(arms)):
#     this_arm = arms[i]
#     this_end = this_arm.get_endpoint()
#     if DEBUG:
#         print("Arm #%d:" % i)
#         print("Starting point")
#         print(this_arm.origin)
#         print("Ending point")
#         print(this_end)
#         print("Moving on to next arm")
#         print("")
#
#     ax.plot([this_arm.origin[0], this_end[0]], [this_arm.origin[1], this_end[1]])

rob.reach([14, -14], dt)
rob.reset(dt)
