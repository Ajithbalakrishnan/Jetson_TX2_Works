# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2
import sys

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


sender = imagezmq.ImageSender(connect_to='tcp://172.16.35.195:5555')
# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
print("rpi name: ", rpiName)
#vs = VideoStream(usePiCamera=True).start()
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
#cap = VideoStream(gstreamer_pipeline(flip_method=0)).start()
time.sleep(2.0)
jpeg_quality = 95
fps = cap.get(cv2.CAP_PROP_FPS)
print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
while True:
	# read the frame from the camera and send it to the server
    ret_val, img = cap.read()
    print("shape : ",img.shape)
    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        #cv2.imshow("CSI Camera", img)
        #keyCode = cv2.waitKey(30) & 0xFF
        #if keyCode == 27:
        #    break
       
      
    sender.send_image(rpiName, jpg_buffer)
