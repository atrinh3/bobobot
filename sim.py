
# coding: utf-8

# In[53]:


import matplotlib.pyplot as plt
import matplotlib.lines as lin
from mpl_toolkits.mplot3d import Axes3D
import math


# In[93]:


class Arm:
    def __init__(self, arm_length, arm_origin, arm_angle):
        self.length = arm_length
        self.origin = arm_origin
        self.angle = arm_angle
    
    def get_endpoint(self):
        # x_end
        x = self.origin[0] + (self.length * math.cos(math.radians(self.angle)))
        
        # y_end
        y = self.origin[1] + 0
        
        # z_end
        z = self.origin[2] + (self.length * math.sin(math.radians(self.angle)))
        
        endpoint = [round(x, 3), round(y, 3), round(z, 3)]
        return endpoint
    
    


# In[121]:


arm1 = Arm(10, [0, 0, 0], -70)
arm2 = Arm(10, arm1.get_endpoint(), 45)
arm3 = Arm(1, arm2.get_endpoint(), 45)


# In[122]:


arms = [arm1, arm2, arm3]


# In[123]:


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(0, len(arms)):
    this_arm = arms[i]
    this_end = this_arm.get_endpoint()
    print("Arm #%d:" % i)
    print("Starting point")
    print(this_arm.origin)
    print("Ending point")
    print(this_end)
    print("Moving on to next arm")
    print("")
    
    ax.plot([this_arm.origin[0], this_end[0]], [this_arm.origin[1], this_end[1]], [this_arm.origin[2], this_end[2]])

