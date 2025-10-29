import numpy as np
import time
import math
import json
import threading
import geometry as gm
import Camera
import cv2
from Shared import therds_stop, hsv_frame_queue
from CVobj import CVobj

with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)


img_resolution = json["resolution"]["img"]

Camera.theard.start()
blue = CVobj("blue", img_resolution,  ((100, 100, 100),(255, 255,255)))  

time.sleep(3)
while True:
    frame = hsv_frame_queue.get()
    cv2.drawContours(frame, blue.glob_contour,5, (255,255,0))
    cv2.imshow("Cap",cv2.cvtColor( cv2.resize(frame, (400,400)), cv2.COLOR_HSV2BGR))
    cv2.imshow("Blueb",cv2.resize(blue.buf,(400,400)))
    try:
        cv2.imshow("Blue",cv2.cvtColor(blue.sect,cv2.COLOR_HSV2BGR))
    except:
        print("0 blue")
    blue.main_calc(frame)
    print(blue.main_vec.leng)
    time.sleep(0.1)
    if cv2.waitKey(5) == 27:
                break
therds_stop.set()
Camera.theard.join()

