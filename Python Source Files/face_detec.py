import os
import subprocess

# OR export QT_QPA_PLATFORM=xcb
# os.environ["QT_QPA_PLATFORM"] = "xcb" # When a monitor is connected
os.environ["QT_QPA_PLATFORM"] = "offscreen" # When a monitor is connected
subprocess.call(['sudo', 'pigpiod'])

import numpy as np
from datetime import datetime
import time
from picamera2 import Picamera2

from servo_ctrl import *
import os
import cv2

# resolution of video recorded
res_width = 640
res_len = 480

# Initialize the camera
picam2 = Picamera2()

# RECORDING VIDEO
#picam2.start_and_record_video('test.mp4', config = vid_cfg, duration = 5, show_preview = False, audio = False)

# Configure the camera for capturing video frames (adjust resolution and format)
video_config = picam2.create_video_configuration(main={"size": (res_width, res_len), "format": 'YUV420'})
#vid_cfg = picam2.create_video_configuration()
picam2.configure(video_config)

# Start the camera
picam2.start()

#Setting up face detection
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# variable required for motion detection
last_mean = 0
min_time_rec = 20	# in sec
det_motion = False

servo_angle = servo_init()

# Loop to capture frames
while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()  # Get the frame as a NumPy array

    if frame is not None:
        # gray = cv2.resize(frame, (640, 480))
        # Convert to greyscale for easier faster accurate face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_I420)
        frame2 = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)	# only for imshow() function - can be disabled
        
        new_mean = np.mean(gray)
        change = new_mean - last_mean
        # print(f"Mean change: {change}")
        
        if abs(change) > 3:
            print("Motion Detected")
            start_time = datetime.now()
            last_mean = new_mean
        
        # If motion is detected, append the frame to the list
        if det_motion:
            rec_time = datetime.now()
            if (rec_time - start_time).total_seconds() > min_time_rec:
                det_motion = False

        gray = cv2.equalizeHist( gray )
        # Do face detection to search for faces from these captures frames
        faces = faceCascade.detectMultiScale(frame, 1.3, 5, 0, (15, 15))		# TODO lot of optimization

        #Below draws the rectangle onto the screen then determines how to move the camera module so that the face can always be in the centre of screen. 
        for (x, y, w, h) in faces:
            print("person detected!")
            # Draw a green rectangle around the face (There is a lot of control to be had here, for example If you want a bigger border change 4 to 8)
            cv2.rectangle(frame2, (x, y), ((x + w), (y + h)), (0, 255, 0), 4)
            cen_w = x - w/2
            cen_l = y - h/2
            print(f"centre: ({cen_w},{cen_l})")
            if cen_w > 240:
                servo_angle = rotate(servo_angle, servo_angle + 5)
            else:
                servo_angle = rotate(servo_angle, servo_angle - 5)
        
        frame2 = cv2.flip(frame2, -1) # vertical flip
        # frame2 = cv2.flip(frame2, 1) # horizontal flip
        # cv2.imshow("Preview", frame2)
        # following statement is required for im show at all costs
        # cv2.waitKey(1)        

# Stop the camera and clean up
picam2.stop()
cv2.destroyAllWindows()
