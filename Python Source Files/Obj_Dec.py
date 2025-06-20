import cv2
import numpy as np
from datetime import datetime
import time
from picamera2 import Picamera2
import subprocess
import os

os.environ["QT_QPA_PLATFORM"] = "xcb"

res_width = 1280
res_len = 720

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

# Set up OpenCV window
# cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)

last_mean = 0
min_time_rec = 20	# in sec
det_motion = False

# Loop to capture frames
while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()  # Get the frame as a NumPy array
    
    if frame is not None:
        # Convert the frame to BGR (OpenCV expects BGR format)
        gray = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(gray, cv2.COLOR_YUV2GRAY_I420)
        new_mean = np.mean(gray)
        change = new_mean - last_mean
        # print(f"Mean change: {change}")
        
        if abs(change) > 2:
            print("Motion Detected")
            start_time = datetime.now()
            last_mean = new_mean
            if (det_motion is False):
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
            det_motion = True
        
        # If motion is detected, append the frame to the list
        if det_motion:
            # frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)  # Convert to BGR for video recording
            # Send the raw frame data to FFmpeg via stdin pipe
            process.stdin.write(frame.tobytes())  # Write frame to the ffmpeg process
            # cv2.imshow('Recording Video', frame_bgr)
            rec_time = datetime.now()
            if (rec_time - start_time).total_seconds() > min_time_rec:
                det_motion = False
                # Gracefully close the subprocess (FFmpeg)
                process.stdin.close()  # Close the stdin pipe
                process.wait()  # Wait for the subprocess to finish
                # cv2.destroyAllWindows()
            
        # Display the frame using OpenCV
        # cv2.imshow("Preview", gray)

# Stop the camera and clean up
picam2.stop()
cv2.destroyAllWindows()
