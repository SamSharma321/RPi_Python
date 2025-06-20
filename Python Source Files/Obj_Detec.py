import cv2
import numpy as np
from datetime import datetime
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, MJPEGEncoder
import os
from servo_ctrl import *
from global_data import *
import subprocess

show_preview = False

#Setting up face detection
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Initialize the camera - picamera module
picam2 = Picamera2()
# Configure the camera for capturing video frames (adjust resolution and format)
video_config = picam2.create_video_configuration(main={"size": (res_width, res_len), "format": 'YUV420'})

def start_rec_blocking(duration = 1000):		# TODO not working bro
    start_time = datetime.now()
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    # Set up the FFmpeg command to capture video
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # Overwrite output file without asking
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'yuv420p',#bgr24',
        '-s', f'{res_width}x{res_len}',  # Resolution
        '-r', '24',  # Frames per second
        '-i', '-',  # Input from stdin (pipe)
        rf'vids/test_{filename}',  # Output file
        '-loglevel', 'error'
    ]
    # Open the subprocess for ffmpeg
    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
    
    if (datetime.now() - start_time).total_seconds() <= duration:
        frame = picam2.capture_array()  # Get the frame as a NumPy array
        if frame is not None:
            # Convert the frame to BGR (OpenCV expects BGR format)
            gray = cv2.resize(frame, (res_width, res_len))
            gray = cv2.cvtColor(gray, cv2.COLOR_YUV2BGR_I420)
            # Send the raw frame data to FFmpeg via stdin pipe
            process.stdin.write(frame.tobytes())  # Write frame to the ffmpeg process
    
    # python code for RECORDING VIDEO
    #vid_cfg = picam2.create_video_configuration()
    #rec_name = 'datetime.now()_recording.mp4'
    #picam2.start_and_record_video(rec_name, config = vid_cfg, duration = 5, show_preview = False, audio = False)
    #picam2.stop()
    return

def init_cam():
    # OR export QT_QPA_PLATFORM=xcb
    os.environ["QT_QPA_PLATFORM"] = "xcb" 

    picam2.configure(video_config)
    # initialize servo module
    global servo_angle
    servo_angle = 180
    servo_init(servo_angle)
    # Start the camera
    picam2.start()


def face_detect_2(frame2):
    bFaceDetec = False
    cen_w = 240
    cen_l = 0
    # Do face detection to search for faces from these captures frames
    faces = faceCascade.detectMultiScale(frame2, 1.4, 4, 0, (30, 30))		# TODO lot of optimization
    #Below draws the rectangle onto the screen then determines how to move the camera module so that the face can always be in the centre of screen. 
    for (x, y, w, h) in faces:
        print("person in frame")
        bFaceDetec = True
        cen_w = x - w/2
        cen_l = y - h/2
        # print(f"centre: ({cen_w},{cen_l})")
        if show_preview:
            # Draw a green rectangle around the face (There is a lot of control to be had here, for example If you want a bigger border change 4 to 8)
            cv2.rectangle(frame2, (x, y), ((x + w), (y + h)), (0, 255, 0), 4)
    if show_preview:
        cv2.imshow("Preview", frame2)
        # following statement is required for im show at all costs
        cv2.waitKey(1)
    return bFaceDetec, cen_w, cen_l
        

def face_detec(frame2):
    global servo_angle
    # Get the details
    bFaceDetec, cen_w, cen_l = face_detect_2(frame2)

    if not(200 <  cen_w < 280):
        if (cen_w > 240):
            servo_angle = rotate(servo_angle, servo_angle - 7)
        elif (cen_w < 240):
            servo_angle = rotate(servo_angle, servo_angle + 7)
                
    return bFaceDetec, frame2
    
    
def search():
    global servo_angle
    bFaceDetec = False
    frame2 = None
    # Do once
    frame = picam2.capture_array()  # Get the frame as a NumPy array
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
        frame = cv2.flip(frame, -1)   # vertical flip
        bFaceDetec, cen_w, cen_l = face_detect_2(frame)
        
    if not bFaceDetec:   
        init_angle = 0
        for i in range(0, 181, 3):
            servo_angle = rotate(init_angle, i)
            init_angle = i
            frame = picam2.capture_array()  # Get the frame as a NumPy array
            if frame is not None:
                frame2 = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)	# only for imshow() function - can be disabled
                # frame2 = frame
                # vertical flip - CAMERA IS HUNG UPSIDE DOWN IN MY CASE
                frame2 = cv2.flip(frame2, -1)   
                if not bFaceDetec:
                    bFaceDetec, cen_w, cen_l = face_detect_2(frame2)
                else:
                    break
            # cv2.imshow("Preview", frame2)
            # cv2.waitKey(1)
    return bFaceDetec, frame2

# Loop to capture frames
def follow_me():
    global last_mean
    global det_motion
    global start_time
    bFaceDetec = False
    # Capture a frame from the camera
    frame = picam2.capture_array()  # Get the frame as a NumPy array
    if frame is not None:
        # gray = cv2.resize(frame, (640, 480))
        # Convert to greyscale for easier faster accurate face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_I420)
        # frame2 = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)	# only for imshow() function - can be disabled
        # frame2 = frame
        frame2 = cv2.flip(gray, -1)   # vertical flip

        new_mean = np.mean(gray)
        change = new_mean - last_mean
        # print(f"Mean change: {change}")
        
        if abs(change) > 3:
            det_motion= True
            print("Motion Detected")
            start_time = datetime.now()
            last_mean = new_mean
        
        # If motion is detected, append the frame to the list
        if det_motion:
            bFaceDetec, frame2 = face_detec(frame2) 
            rec_time = datetime.now()
            if ((rec_time - start_time).total_seconds() > min_time_rec) and (not bFaceDetec):
                ret, frame2 = search()
                if not ret:
                    det_motion = False
                    servo_angle = rotate(servo_angle, 180)
        
        # frame2 = cv2.flip(frame2, 1) # horizontal flip
        # cv2.imshow("Preview", frame2)
        # following statement is required for im show at all costs
        # cv2.waitKey(1)
    return bFaceDetec

# init_cam()
#det_motion, frame2 = search()
#start_rec_blocking()
#while True:
#    follow_me()

# Stop the camera and clean up
#picam2.stop()
#cv2.destroyAllWindows()

