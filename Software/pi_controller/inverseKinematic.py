

import math
#import serial
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class scaraRobot():


    def __init__(self):
        self.A=1
        self.B=1
        self.origineX=0
        self.origineY=0
        self.theta01Init=0
        self.theta01Init=0
        self.anglesActuel=[0,0]
        return

    def __int__(self,A0,B0,origine0X,origine0Y,theta01Init,theta02Init):
        self.A = A0
        self.B = B0
        self.origineX = origine0X
        self.origineY = origine0Y
        self.theta01Init = theta01Init
        self.theta01Init = theta02Init
        return


    def setLongueurSegmentA(self,A0):
        self.A=A0
        return

    def setLongueurSegmentB(self,B0):
        self.B=B0
        return

    def getLongueurSegmentA(self):
        return self.A

    def getLongueurSegmentB(self):
        return self.B

    def getAngleDeg(self):
        return [math.degrees(self.anglesActuel[1]),math.degrees(self.anglesActuel[2])]

    def getAngleRad(self):
        return self.anglesActuel

    #def relativePosition(self,0x,0y)

    #return

    def setAnglesAtStart(self,theta01Init,theta02Init):
        self.theta01Init=theta01Init
        self.theta02Init=theta02Init
        return

    def inverseKinematic(self,x,y):
        #TO DO
        #gerer la plage de position acceptable
        #gerer offset origine camera
        #gerer position home robot
        x=x+self.origineX
        y=y+self.origineY

        #gerer elbow down or Up avec le cadran

        B=(math.pow(x,2)+math.pow(y,2)-math.pow(self.A,2)-math.pow(self.B,2))/(2*self.A*self.B)
        theta2=math.atan2(math.sqrt(1-math.pow(B,2)),B)
        theta1=math.atan2(y,x)-math.atan2((self.B*math.sin(theta2)),(self.A+self.B*math.cos(theta2)))
        self.anglesActuel=[theta1,theta2]
        return self.anglesActuel

def positionSegment2d(r,target):
    """Segment generation"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #segment A
    aX, aY, aZ = r.getLongueurSegmentA()*math.cos(r.getAngleRad()[0]), r.getLongueurSegmentA()*math.sin(r.getAngleRad()[0]), 0
    ax.cla()
    #segment B
    ax.quiver(0, 0, 0, aX, aY, aZ, pivot="tail", color="black")
    bx, by, bz = r.getLongueurSegmentB() * math.cos(r.getAngleRad()[1]+r.getAngleRad()[0]), r.getLongueurSegmentA() * math.sin(r.getAngleRad()[1]+r.getAngleRad()[0]), 0
    ax.quiver(aX, aY, aZ, bx, by, bz, pivot="tail", color="red")

    ax.plot(target[0],target[1], 1, 'bo', label='marker only')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.view_init(elev=-270, azim=-90)

   # ani = animation.FuncAnimation(fig, data_gen, range(72), blit=False)
    plt.show()
    return



#arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

# def write_read(x):
# 	arduino.write(bytes(x, 'utf-8'))
# 	time.sleep(0.5)
# 	data = arduino.readline()
# 	return data

# def send_angle(self, robot):
#     angles=robot.positionToAngleRad(input("Enter position in X :"), input("Enter position in X :"))
#     aAngle = angles[1]
#     bAngle = angles[2]
#     zHeigh = input("Enter a height for Z :")
#     testString = "G0:A" + str(aAngle) + ":B" + str(bAngle) + ":Z" + zHeigh + "\r\n"
#     value = write_read(testString)
#     print(value)
#     return 1

if __name__ == '__main__':

    target=[0,2]
    r = scaraRobot()
    print(r.inverseKinematic(target[0],target[1]))
    positionSegment2d(r,target)

