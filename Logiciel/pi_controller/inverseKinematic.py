

import math
#import serial
import matplotlib.pyplot as plt


class scaraRobot():


    def __init__(self):
        self.A=0.2001
        self.B=0.25212
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

    def isInEnvloppe(self, x, y):
        if math.sqrt(math.pow(x, 2) + math.pow(y, 2)) <= (self.A + self.B) and math.sqrt(
                math.pow(x, 2) + math.pow(y, 2)) >= (0.15):



            return True
        else:
            return False

    def inverseKinematic(self,x,y):
        #TO DO
        #gerer la plage de position acceptable en y neg


        x=x+self.origineX
        y=y+self.origineY
        if self.isInEnvloppe(x,y):

            B=(math.pow(x,2)+math.pow(y,2)-math.pow(self.A,2)-math.pow(self.B,2))/(2*self.A*self.B)

            theta2=math.atan2(math.sqrt(1-math.pow(B,2)),B)
            if x >= 0:
               #config upper shoulder
                theta2=-theta2
            theta1=math.atan2(y,x)-math.atan2((self.B*math.sin(theta2)),(self.A+self.B*math.cos(theta2)))

            self.anglesActuel=[theta1,theta2]

            return  [math.degrees(theta1), math.degrees(theta2)]
        else:
            return False


    def forwardKinematic(self):
        x1=self.A*math.cos(self.anglesActuel[0])
        x2=x1+self.B*math.cos(self.anglesActuel[0]+self.anglesActuel[1])

        y1 = self.A * math.sin(self.anglesActuel[0])
        y2 = y1 + self.B * math.sin(self.anglesActuel[0] + self.anglesActuel[1])

        return [x2,y2]



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

    ax.plot(target[0],target[1], 0, 'bo', label='marker only')
    ax.set_xlim(-0.3, 0.3)
    ax.set_ylim(-0.3, 0.3)
    ax.set_zlim(-0.3, 0.3)
    ax.view_init(elev=-270, azim=-90)

    plt.show()
    return



arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def write_read(x):
	arduino.write(bytes(x, 'utf-8'))
	time.sleep(0.5)
	data = arduino.readline()
	return data

# def send_angle(self, robot):
#     angles=robot.positionToAngleRad(input("Enter position in X :"), input("Enter position in y :"))
#     aAngle = angles[1]
#     bAngle = angles[2]
#     zHeigh = input("Enter a height for Z :")
#     testString = "G0:A" + str(aAngle) + ":B" + str(bAngle) + ":Z" + zHeigh + "\r\n"
#     value = write_read(testString)
#     print(value)
#     return 1

if __name__ == '__main__':
    target = [0.2, 0.2]
    print("target= ", [0.2,0.2])
    r = scaraRobot()
    angles=r.inverseKinematic(target[0],target[1])
    print("theta 1 deg : ", angles[0],"\ntheta 2 deg : ",angles[1])
    print("forward kinematic result ",r.forwardKinematic())

    # for y in np.arange(0,0.45,0.01):
    #     for x in np.arange(0,0.45,0.01):
    #         if r.inverseKinematic(x,y) is not False:
    #
    positionSegment2d(r,target)




