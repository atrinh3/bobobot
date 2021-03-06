from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.lines as lin
from time import time
import numpy as np
import math

DEBUG = False


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
        self.torque = 1  # 1 deg / sec

    def position(self):
        return self.arm2.get_endpoint()

    def get_x(self):
        x = [self.arm1.origin[0], self.arm2.origin[0], self.position()[0]]
        return x

    def get_y(self):
        y = [self.arm1.origin[1], self.arm2.origin[1], self.position()[1]]
        return y

    def reach(self, new_target):
        print("Reaching for target")
        # if "under the table" may have to move arm1 back to
        # retract arm2 first before moving above the table

        # angle to target
        self.target = new_target
        self.moving = True

    def reset(self):
        print("Resetting arms :)")
        self.reach([10, -10])

    def target_prox(self):
        return math.hypot(self.target[0] - self.position()[0],
                          self.target[1] - self.position()[1])

    def in_range(self):
        # return if arm2 can reach without arm1 moving
        distance = math.hypot(self.target[0] - self.arm2.origin[0],
                              self.target[1] - self.arm2.origin[1])
        return abs(distance - self.arm2.length) < 1

    def move_arm1(self, distance):
        if not self.in_range():
            self.arm1.move(distance)
            self.arm2.set_origin(self.arm1.get_endpoint())

    def move_arm2(self, distance):
        if self.target_prox() < 2:
            self.arm2.move(distance)
            self.moving = False

    def step(self, dt):
        while self.moving:
            # find direction to move arm1
            a1_limit = math.degrees(math.atan(self.target[0] / self.target[1]))

            # adjust arm1 by some degrees
            self.move_arm1(np.sign(a1_limit - self.arm1.angle) * self.torque * dt)

            # find new angle for arm 2 resulting from arm1 movement
            a2_target = math.degrees(math.atan((self.target[1] - self.position()[1]) /
                                               (self.target[0] - self.position()[0])))
            # adjust arm2 by some degrees
            self.move_arm2(np.sign(a2_target - self.arm2.angle) * self.torque * dt)
        self.time_elapsed += dt


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

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 25), ylim=(-20, 10))

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

dt = 1 / 60  # 30fps
t = np.arange(0.0, 10, dt)
line, = ax.plot([], [], lw=2)
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text("")
    return line, time_text


def animate(i):
    global rob, dt
    rob.step(dt)
    if rob.time_elapsed > 1:
        rob.reach([13, -10])
    line.set_data(rob.get_x(), rob.get_y())
    time_text.set_text("time = %.1f" % rob.time_elapsed)
    return line, time_text


t0 = time()
animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=300, interval=interval, blit=True, init_func=init)
plt.show(block=True)

