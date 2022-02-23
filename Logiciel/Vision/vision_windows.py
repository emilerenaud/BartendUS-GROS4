import numpy as np
from PIL import Image
import cv2

def vision():
    path = r"pic.jpeg"
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    ret, frame = cap.read()
    cv2.imwrite(path, frame)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    im = Image.open(path).convert('L') #.resize([10000, 10000])
    pixel = im.load()
    x =0
    y =0
    nb =0
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pixel[i,j] > 150:
                im.putpixel([i,j], 255)
                x += i
                nb += 1
                y += j
            else:
                im.putpixel([i,j], 0)

    x = int(x/nb)
    y = int(y/nb)
    coord = [x, y]
    return coord

print(vision())