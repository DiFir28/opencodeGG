import numpy as np
import time
import math
import json
import threading
import geometry as gm
# import Camera
import cv2
from Shared import therds_stop, hsv_frame_queue, coords
# import CVobj
import SArduino
import Coordinates
# from Strateg_classes import horOut

import Coordinates

last_ballIn=0
last_ball_time = 0
recessHsum=0

# def ballIn():
#      global last_ballIn, recessHsum, last_ball_time
#      if last_ballIn == 1:
#            if CVobj.orange.main_vec.leng <100:
#                  return 1

#      hsv = hsv_frame_queue.get()
#      hsv_frame_queue.put(hsv)

#      recessHsum = np.sum(hsv[865:900, 952:992, 0])
#      # print(recessHsum)

#      if CVobj.orange.main_vec.leng <98 :
#            last_ballIn = 1
#            return 1
#      else:
#            last_ballIn =0
#            last_ball_time = time.time()
#            return 0



with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)


SArduino.thread.start()

# Camera.theard.start()
# CVobj.theard.start()
Coordinates.thread.start()


# if json["op_goal"] == "Blue":
#      op_goal = CVobj.blue
# else:
#      op_goal = CVobj.yellow
      

time.sleep(3)
gyro = 0
last_ball_d = 0
flag = 0 

lin_dir = 0
lin_vel = 0
rot_dir = 0 
drib_pow = 0
qq = 0

try:
     while True:

          st=gm.point(50,30)

          robot_pos=gm.point(coords[0],coords[1])
          
          dirr=gm.vec()
          dirr.beg=robot_pos
          dirr.end=st
          dirr.calcang()
          print(coords, dirr.ang)

          if gm.ro(st,robot_pos)>10:
               lin_vel=1000
          else:
               lin_vel=0
     

          SArduino.write_to_arduino(f',{round(dirr.ang*1000)}, {lin_vel}, {rot_dir}, {drib_pow},{7000},')

          # frame = hsv_frame_queue.get()
          # if CVobj.blue.ret:
          #      cv2.drawContours(frame, CVobj.blue.glob_contour,5, (255,255,0))
          # cv2.imshow("Cap",cv2.cvtColor( cv2.resize(frame, (400,400)), cv2.COLOR_HSV2BGR))
          # print(CVobj.blue.main_vec.leng, np.shape(CVobj.blue.sect))
          # if cv2.waitKey(5) == 27:
          #                     break

          # try:
          #      cv2.imshow("Blue",cv2.cvtColor(CVobj.blue.sect,cv2.COLOR_HSV2BGR))
          # except:
          #      print("0 blue")
     # blue.main_calc(frame)
     # print(blue.main_vec.leng)

     '''     
          try:
               gyro = float(ser_theard.data)
               # gyro *= 1000
          except:
               print("OG ", end = "")
          time.sleep(0.01)
          
          # print(CVobj.blue.main_vec.ang, CVobj.yellow.main_vec.ang, CVobj.orange.main_vec.ang)
          # if abs(CVobj.orange.main_vec.ang+ 1.571) > 0.1:
          #      lin_dir = 0
          #      lin_vel = 0
          #      rot_dir = 1571+round(1000*(CVobj.orange.main_vec.ang+gyro))

          # else:
          if ballIn() == 0:
               lin_dir = 1571+round(1000*(CVobj.orange.main_vec.ang+gyro))
               lin_vel = 100 + round(CVobj.orange.main_vec.leng)*3
               rot_dir = 1571+round(1000*(CVobj.orange.main_vec.ang+gyro))
               if CVobj.orange.main_vec.leng < 140:
                    drib_pow= 100
               else:

                    drib_pow= 50
          else:
               if time.time() - last_ball_time < 3:
                    lin_vel = 100
                    rot_dir = 1571+round(1000*(CVobj.orange.main_vec.ang+gyro))
                    drib_pow= 70
               elif time.time() - last_ball_time < 7:
                    lin_vel = 0
                    rot_dir = 1571+round(1000*(op_goal.main_vec.ang+gyro - 3142))                    
                    drib_pow= 80
               else:
                    lin_vel = 0
                    rot_dir = 1571+round(1000*(op_goal.main_vec.ang+gyro))                    
                    drib_pow= 150
     


          print(CVobj.orange.main_vec.ang, CVobj.orange.main_vec.leng, gyro, ballIn(), time.time() - last_ball_time, abs(CVobj.orange.main_vec.ang+ 1.571), lin_vel)


          # if ballIn() == 0:
          #      lin_dir = 1571+round(1000*(CVobj.orange.main_vec.ang+gyro))
          #      lin_vel = 100 + round(CVobj.orange.main_vec.leng) * 9
          #      rot_dir = 1571+round(1000*(CVobj.orange.main_vec.ang+gyro))
          #      if CVobj.orange.main_vec.leng < 140:
          #           drib_pow= 50
          #      else:

          #           drib_pow= 40
          # else:
          #       lin_vel =0
                

           

          ser_theard.write_to_arduino(f',{lin_dir}, {lin_vel}, {rot_dir}, {drib_pow},{7000},')
          last_ball_d = CVobj.orange.main_vec.leng
          '''
          
except KeyboardInterrupt:
     print("Break")  
finally:
     SArduino.write_to_arduino(f',{0}, {0}, {0}, {0}, {5000},')
     therds_stop.set()
     # Camera.theard.join()
     Coordinates.thread.join()


