import numpy as np
import time
import math
import json
import threading
import geometry as gm
import Camera
import cv2
from Shared import therds_stop, hsv_frame_queue
import CVobj
import ser_theard

def ballIn():
     hsv = hsv_frame_queue.get()
     hsv_frame_queue.put(hsv)

     recessHsum = np.sum(hsv[860:900, 952:992, 0])

     if (60000<recessHsum and recessHsum<80000) and (CVobj.orange.main_vec.leng <95 or CVobj.orange.main_vec.leng>130):
           return 1
     else:
           return 0



with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

read_thread = threading.Thread(target=ser_theard.read_from_arduino)
read_thread.daemon = True
read_thread.start()

Camera.theard.start()
CVobj.theard.start()

time.sleep(3)
gyro = 0
last_ball_d = 0
flag = 0 
try:
     while True:
     # frame = hsv_frame_queue.get()
     # if CVobj.blue:
     #     cv2.drawContours(frame, CVobj.blue.glob_contour,5, (255,255,0))
     # cv2.imshow("Cap",cv2.cvtColor( cv2.resize(frame, (400,400)), cv2.COLOR_HSV2BGR))
     # cv2.imshow("Blueb",cv2.resize(blue.buf,(400,400)))
     # try:
     #     cv2.imshow("Blue",cv2.cvtColor(blue.sect,cv2.COLOR_HSV2BGR))
     # except:
     #     print("0 blue")
     # blue.main_calc(frame)
     # print(blue.main_vec.leng)
          
          try:
               gyro = float(ser_theard.data)
               # gyro *= 1000
          except:
               print("OG ", end = "")
          time.sleep(0.01)
          
          print(CVobj.orange.main_vec.ang, CVobj.orange.main_vec.leng, gyro, ballIn(), end = "\r")

           

          ser_theard.write_to_arduino(f',{1571+round(1000*(CVobj.orange.main_vec.ang+gyro))}, {(1-flag)*2000}, {1571+round(1000*(CVobj.orange.main_vec.ang+gyro))}, {drib_pow}, {5000},')
          last_ball_d = CVobj.orange.main_vec.leng
          if cv2.waitKey(5) == 27:
                         break
except KeyboardInterrupt:
     print("Break")  
finally:
     ser_theard.write_to_arduino(f',{0}, {0}, {0}, {70 * (CVobj.orange.main_vec.ang<100)}, {5000},')
     therds_stop.set()
     Camera.theard.join()

