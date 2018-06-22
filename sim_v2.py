
# coding: utf-8

# In[51]:


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.lines as lin
from time import time
import numpy as np
import math

DEBUG = False


# In[114]:


class Bobo:
    def __init__(self, arms):
        self.arms = arms
        self.arm1 = arms[0]
        self.arm2 = arms[1]
        self.angle1 = arm1.angle
        self.angle2 = arm2.angle
        self.position = arms[1].get_endpoint()
        self.w1 = 0
        self.w2 = 0
        self.time_elapsed = 0
        self.target = self.arm2.get_endpoint()
        self.moving = False
        self.torque = 1.2  # 1 deg / sec
    
    def update_position(self):
        self.position = self.arm2.get_endpoint()

    def get_x(self):
        x = [self.arm1.origin[0], self.arm2.origin[0], self.position()[0]]
        return x

    def get_y(self):
        y = [self.arm1.origin[1], self.arm2.origin[1], self.position()[1]]
        return y

    def reach(self, new_target, dt):
        if DEBUG:
            print("Reaching for target")
        # if "under the table" may have to move arm1 back to
        # retract arm2 first before moving above the table

        # angle to target
        self.target = new_target
        self.moving = True
        self.step(dt)

    def reset(self, dt):
        if DEBUG:
            print("Resetting arms :)")
        self.reach([10, -10], dt)

    def distance(self, coordinate):
        return math.hypot(coordinate[0], coordinate[1])
    
    def angle(self, coordinate):
        return math.degrees(math.atan(coordinate[1] / coordinate[0]))

    def move_arm1(self, distance):
        self.arm1.move(distance)
        self.arm2.set_origin(self.arm1.get_endpoint())

    def proximity(self):
        a = self.position[0] - self.target[0]
        b = self.position[1] - self.target[1]
        return math.hypot(a, b)
        
    def move_arm2(self, distance):
        if self.proximity() > .5:
            self.arm2.move(distance)
            self.update_position()
            if DEBUG:
                print(str(self.proximity()) + " away from the target position")
        else:
            self.moving = False
            if DEBUG:
                print("self.moving now = False")

    def a1_target(self, target):
        # There should almost always be 2 points where the arm is in range
        # Pick the one that has the lower value.
        d_target = self.distance(target)
        a_target = self.angle(target)
        out = self.arms[0].length * self.arms[0].length
        out += d_target * d_target
        out -= self.arms[1].length * self.arms[1].length
        out = out / (2 * self.arms[0].length * d_target)
        out = -math.degrees(math.acos(out)) + a_target
        
        if DEBUG:
            print("Target angle for arm1: " + str(out))
            x = arm1.length * math.cos(math.radians(out))
            y = arm1.length * math.sin(math.radians(out)            )
            print("Target position for arm1: ({x}, {y})".format(x=x, y=y))
        return out        
        
    def step(self, dt):
        if self.moving:
            # find direction to move arm1
            a1_aim = self.a1_target(self.target)
            if DEBUG:
                print("Target angle for arm 1: " + str(a1_aim))
            a1_x = self.arms[0].length * math.cos(math.radians(a1_aim))
            a1_y = self.arms[0].length * math.sin(math.radians(a1_aim))
            a2_target = math.degrees(math.atan((self.target[1] - a1_y) / (self.target[0] - a1_x)))

            # find new angle for arm 2 resulting from arm1 movement
            if DEBUG:
                print("{time} - Current Position: {pos}, target: {target}".format(
                        time=self.time_elapsed, pos=self.position, target=self.target))            
            while self.moving:
                # adjust arm1 by some degrees
                if abs(a1_aim - self.arm1.angle) >= .5:
                    self.move_arm1(np.sign(a1_aim - self.arm1.angle) * self.torque * dt)
                    
                # aim arm2 based on predicted movement of arm1
                self.move_arm2(np.sign(a2_target - self.arm2.angle) * self.torque * dt)
                self.time_elapsed += dt
                if DEBUG:
                    a1_end = self.arm1.get_endpoint()
                    print("{time} - Current Position: {pos}, target: {target}".format(
                        time=self.time_elapsed, pos=self.position, target=self.target))
                    print("Current Arm 1 position: ({x}, {y})".format(x=a1_end[0], y=a1_end[1]))
                    print("")
            if DEBUG:
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


# In[115]:


arm1 = Arm(10, [0, 0], -90)
arm2 = Arm(10, arm1.get_endpoint(), 0)
arms = [arm1, arm2]
rob = Bobo(arms)

dt = 1/30 

rob.reach([13, -13], dt)

show_arms(rob)


# In[116]:


rob.reset(dt)
show_arms(rob)


# In[117]:


rob.reach([17, -10], dt)
show_arms(rob)


# In[118]:


rob.reach([10, -8], dt)
show_arms(rob)


# In[119]:


rob.reach([1, -19], dt)
show_arms(rob)


# In[74]:


def show_arms(rob):
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 25), ylim=(-20, 10))

    for i in range(0, len(rob.arms)):
        this_arm = rob.arms[i]
        this_end = this_arm.get_endpoint()
        if DEBUG:
            print("Target: " + str(rob.target))
            print("Arm #%d:" % i)
            print("Starting point")
            print(this_arm.origin)
            print("Ending point")
            print(this_end)
            print("Moving on to next arm")
            print("")

        ax.plot([this_arm.origin[0], this_end[0]], [this_arm.origin[1], this_end[1]])
        ax.plot(rob.target[0], rob.target[1], marker="x")

