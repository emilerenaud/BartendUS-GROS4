import numpy as np
from PIL import Image
import subprocess

def vision():
    output = False # False: Disable display output & True: Enable display output
    subprocess.run("sudo fswebcam /home/pi/Desktop/Frame.jpg", capture_output=True)
    #path = r"C:\Users\thephysicist\Desktop\pic.jpeg"
    path = r'/home/pi/Desktop/Frame.jpg'

    imcolor = Image.open(path)
    im = imcolor.convert('L')
    pixel = im.load()
    x =0
    y =0
    nb =0
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if j > (im.size[1]-200):
                im.putpixel([i,j], 0)
            elif j < (0):
                im.putpixel([i,j], 0)
            elif i > (im.size[0]-0):
                im.putpixel([i,j], 0)
            elif i < (0):
                im.putpixel([i,j], 0)
            elif pixel[i,j] > 220:
                x += i
                nb += 1
                y += j
    x = int(x/nb)
    y = int(y/nb)
    coord = [(0.20*(x-(im.size[0]/2))/(im.size[0]/2)), (0.20*(y)/(im.size[1]/2))] #[x,y] in meters, origin at the A axis
    if output:
        for i in range(x-10,x+10,1):
            for j in range(y-10,y+10,1):
                imcolor.putpixel([i,j], (255,0,0))
        imcolor.show()
    return coord

print(vision())