import time
import numpy as np
import json
import cv2
import math
from picamera2 import Picamera2
from CVobj import CVobj, find_contour, cent_contour
import geometry as *


# Camera settings 
cap_resolution = (2304, 1296)
img_resolution = (1296, 1296)
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
   "AfMode": 0,            # 0 = Manual
    "LensPosition":21.0 
    # "ExposureTime": 25000,  
    # "AeEnable": False,    
    # "AwbEnable": False, 
    
})
time.sleep(2)
# cap.set_controls({"Transform": {"hflip": True, "vflip": False}})



# CV init

# Theard defenition

cap.start()

def cap_read():
    global cap, raw_frame_bgr, raw_frame_hsv

    raw_frame_bgr = cv2.cvtColor(cap.capture_array(), cv2.COLOR_RGB2BGR) 
    raw_frame_hsv = cv2.cvtColor(raw_frame_bgr, cv2.COLOR_BGR2HSV) 


yellow = CVobj("Y", (2304, 1296), ((10,100,100),( 30, 255, 255 )))

blue = CVobj("B", (2304, 1296), ((100,100,80),( 270, 255, 255 )))
while True:

    cap_read()
    cv2.circle(raw_frame_bgr, (1152, 648), 30, (0,0,0), 6)
    # _, cnt,_ = find_contour(raw_frame_hsv, ((100,100,80),( 270, 255, 255 )))
    # cv2.drawContours(raw_frame_bgr,cnt,-1, (255,0,0),5)
    # cx, cy = cent_contour(cnt)
    # print(math.sqrt((cx-1152)**2 + (cy-648)**2))
    yellow.main_calc(raw_frame_hsv)
    blue.main_calc(raw_frame_hsv)

    # cv2.drawContours(raw_frame_bgr, yellow.loc_contour ,-1, (255,0,0),5)
    # print(yellow.main_vec.leng, yellow.main_vec.end)

    x, y = tup((yellow.main_vec.end))
    cv2.circle(raw_frame_bgr, (x , y), radius=10, color=(0, 0, 250), thickness=-1)
    x, y = tup((blue.main_vec.end))
    cv2.circle(raw_frame_bgr, (x , y), radius=10, color=(250, 0, 250), thickness=-1)
    

    cv2.imshow("Frame", cv2.resize(raw_frame_bgr,((1080, 607))))
    cv2.imshow("Bool", cv2.cvtColor(yellow.buf, cv2.COLOR_HSV2BGR))

    
        
    if cv2.waitKey(5) == 27:
        break

cv2.imwrite("test_brg.jpg", raw_frame_bgr)
cap.stop()
cap.close()
cv2.destroyAllWindows()
print("F")