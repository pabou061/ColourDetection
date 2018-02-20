import numpy as np
import cv2

def drawcircle(
    low,
    high,
    frame,
    color,
    ):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    res = cv2.inRange(hsv, low, high)
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(res, kernel, iterations=2)
    dilation = cv2.dilate(erosion, kernel, iterations=2)

##    blur = cv2.GaussianBlur(dilation,(5,5),3)

    (im2, contours, hierarchy) = cv2.findContours(dilation,
            cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

##  only proceed if at least one contour was found

    if len(contours) > 0:

##            find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid

        for c in contours:

            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > 12 and radius < 100:
                cv2.circle(frame, (int(x), int(y)), int(radius + 15),
                           (0, 255, 255), 2)
                cv2.putText(
                    frame,
                    color,
                    (int(x + 60), int(y)),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    0,
                    )
                cv2.putText(
                    frame,
                    'x=' + str(int(x)),
                    (int(x + 60), int(y + 15)),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    0,
                    )
                cv2.putText(
                    frame,
                    'y= ' + str(int(y)),
                    (int(x + 60), int(y + 30)),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    0,
                    )

    return frame


vid = cv2.VideoCapture('videos/video1.mp4')

##get all properties

count = int(vid.get(7))
width = int(vid.get(3))
height = int(vid.get(4))
framerate = int(vid.get(5))

##create an empty video to save all our new frames

out = cv2.VideoWriter('result.avi', -1, framerate, (width, height), 1)

##green

lower_color_green = np.array([45, 100, 100])
upper_color_green = np.array([93, 255, 255])

##yellow

lower_color_yellow = np.array([19, 100, 100])
upper_color_yellow = np.array([35, 255, 255])

##red

lower_color_red = np.array([0, 151, 50])
upper_color_red = np.array([4, 255, 255])

##blue

lower_color_blue = np.array([0, 0, 0])
upper_color_blue = np.array([55, 255, 255])

##loop through all the frames

while vid.isOpened():

##vid.set(1,frame_no)

##read current frame

    (ret, frame) = vid.read()

##in case of error:

    if ret == False:
        break
    else:
        frame = drawcircle(lower_color_yellow, upper_color_yellow,
                           frame, 'yellow')
        frame = drawcircle(lower_color_red, upper_color_red, frame,
                           'red')
        frame = drawcircle(lower_color_green, upper_color_green, frame,
                           'green')
        frame = drawcircle(lower_color_blue, upper_color_blue, frame,
                           'blue')

        out.write(frame)

###release the resources

vid.release()
out.release()
print 'done'
