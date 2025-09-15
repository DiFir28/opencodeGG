import time
import numpy as np
import json

from picamera2 import Picamera2
import cv2

# Camera settings 
cap_resolution = (1280, 960)
img_resolution = (960, 960)
raw_frame_hsv = np.zeros( (img_resolution[0], img_resolution[1], 3), dtype = np.uint8)
raw_frame_bgr = np.zeros( (img_resolution[0], img_resolution[1], 3), dtype = np.uint8)

# CV settings

# Camera init

cap = Picamera2()

config = cap.create_preview_configuration(
    main={"format": "BGR888", "size": cap_resolution,},
    raw={"size": cap.sensor_resolution,},            
    sensor={"output_size": cap_resolution,}
)
cap.configure(config)

cap.set_controls({
    # "ExposureTime": 25000,  
    # "AeEnable": False,    
    # "AwbEnable": False, 
    
})
# cap.set_controls({"Transform": {"hflip": True, "vflip": False}})



# CV init

# Theard defenition

cap.start()

def cap_read():
    global cap, raw_frame_bgr, raw_frame_hsv

    raw_frame_bgr = cv2.cvtColor(cap.capture_array(), cv2.COLOR_RGB2BGR) 
    raw_frame_hsv = cv2.cvtColor(raw_frame_bgr, cv2.COLOR_BGR2HSV) 



while True:

    cap_read()
    cv2.rectangle(raw_frame_bgr, (10,10), (30, 200), (100,100,0), -1)

    cv2.imshow("Frame", raw_frame_bgr)

    
        
    if cv2.waitKey(5) == 27:
        break

cv2.imwrite("test_brg.jpg", raw_frame_bgr)
cap.stop()
cap.close()
print("F")