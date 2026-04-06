import time
import numpy as np
import json
import cv2
import math
import threading
from picamera2 import Picamera2
from Shared import therds_stop, hsv_frame_queue
from geometry import *



# Camera settings 
with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

cap_resolution = json["resolution"]["cap"]
img_resolution = json["resolution"]["img"]
raw_frame_hsv = np.zeros( (img_resolution[0], img_resolution[1], 3), dtype = np.uint8)
raw_frame_bgr = np.zeros( (img_resolution[0], img_resolution[1], 3), dtype = np.uint8)

overlay = cv2.imread("fra.png", cv2.IMREAD_UNCHANGED)
alpha = overlay[:, :, 3] / 255.0
alpha = alpha[:, :, np.newaxis]  # делаем (h, w, 1)

# Camera init
cap = Picamera2()

config = cap.create_preview_configuration(
    main={"format": "BGR888", "size": cap_resolution,},
    raw={"size": cap.sensor_resolution,},            
    sensor={"output_size": cap_resolution,}
)
cap.configure(config)

# cap.set_controls({wher
    #"AfMode": 0,            # 0 = Manual?
    #"LensPosition":40
    # "Contrast" : 1.1,
    # "ExposureTime": 25000,  
    # "AeEnable": False   
    # "AwbEnable": False, 
    
# })
time.sleep(2)


# Theard defenition



dcapx = cap_resolution[0] - img_resolution[0]
dcapy = cap_resolution[1] - img_resolution[1]
def cap_read():
    global cap, raw_frame_bgr, raw_frame_hsv
    raw_frame_bgr = cv2.cvtColor(cap.capture_array(), cv2.COLOR_RGB2BGR) 
    raw_frame_bgr = raw_frame_bgr[(cap_resolution[1] - img_resolution[1])//2 : (cap_resolution[1] - (cap_resolution[1] - img_resolution[1])//2),(cap_resolution[0] - img_resolution[0])//2 : (cap_resolution[0] - (cap_resolution[0] - img_resolution[0])//2)]
#     cv2.circle(raw_frame_bgr, (img_resolution[0]//2, img_resolution[1]//2), 1080, (0,0,0), 530)
    cv2.circle(raw_frame_bgr, (img_resolution[0]//2, img_resolution[1]//2), 120, (10,0,0), -1)
    # cv2.circle(raw_frame_bgr, (img_resolution[0]//2, img_resolution[1]//2), 250, (0,200,0), 1)

    raw_frame_hsv = cv2.cvtColor(raw_frame_bgr, cv2.COLOR_BGR2HSV) 


def theard_reading_cap():
    cap.start()
    while not(therds_stop.is_set()):
        cap_read() 
        if hsv_frame_queue.full():
            hsv_frame_queue.get_nowait()
        hsv_frame_queue.put(raw_frame_hsv)
    cap.stop()
    cap.close()
    

theard = threading.Thread(target = theard_reading_cap, daemon = False)

if __name__ == "__main__":
    cap.start()
    while True:
        print(np.shape(raw_frame_bgr))
        cap_read()
#         cv2.circle(raw_frame_bgr, (img_resolution[0]//2, img_resolution[1]//2), 30, (0,0,0), 6) 
        #img_ = alpha * overlay[:, :, :3] + (1 - alpha) * raw_frame_bgr
        #img_ = img_.astype(np.uint8)
        cv2.imshow("Frame", cv2.resize(raw_frame_bgr, (600,600)))        
            
        if cv2.waitKey(5) == 27:
            break

    cv2.imwrite("test_brg.jpg", raw_frame_bgr)
    cap.stop()
    cap.close()
    cv2.destroyAllWindows()
    print("F")