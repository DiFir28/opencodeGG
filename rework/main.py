import numpy as np
import time
import math
import json
import threading
import geometry as gm
import Camera
import cv2
from Shared import therds_stop, hsv_frame_queue, coords
import CVobj
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

Camera.theard.start()
CVobj.theard.start()
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

while not coords[3]:
     time.sleep(0.1)
     pass


pos_last_err = 0

vel_k = 10

def goToPos(pos):
     global pos_last_err

     if abs(pos.x) >70:
          pos.x=70*gm.sign(pos.x)
     
     if abs(pos.y) >80:
          pos.y=80*gm.sign(pos.y)

     robot_pos=gm.point(coords[0],coords[1])
     dirr=gm.vec()
     dirr.beg=robot_pos
     dirr.end=pos
     dirr.calcang()

     pos_err = dirr.leng
     vel = pos_err*6.0 + (pos_err-pos_last_err)*15.0
     vel=max((vel*vel_k),1000)

     pos_last_err = pos_err

     


     # SArduino.write_to_arduino(f',{round(dirr.ang*1000)}, {lin_vel}, {rot_dir}, {drib_pow},{7000},')

     return (dirr.ang-3.1415926/2), vel


def goIn(pos):
     robot_pos=gm.point(coords[0],coords[1])
     while abs(gm.ro(robot_pos,pos))>10:
          robot_pos=gm.point(coords[0],coords[1])

          # print(coords)
          re=goToPos(pos)
          SArduino.send_int16_array([round(re[0]*1000),round(re[1]),0,0,2000])
          time.sleep(0.01)
     
     





try:
     print("start")
     while True:
          # re=goToPos(gm.point(0,0))
          print(CVobj.orange.main_vec.ang)
          SArduino.send_int16_array([0,0,round((-CVobj.orange.main_vec.ang+gyro)*1000),0,2000])
          time.sleep(0.01)

          # goIn(gm.point(50,0))
          # print(111)
          # time.sleep(0.5)
          # goIn(gm.point(-50,50))
          # time.sleep(0.5)
          # goIn(gm.point(50,50))
          # time.sleep(0.5)

          

          
          
          

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
     SArduino.send_int16_array([0,0,0,0,0])
     print("Break")  
finally:
     print("123")
     SArduino.send_int16_array([0,0,0,0,0])
     print("send")
     
     therds_stop.set()
     Camera.theard.join()
     Coordinates.thread.join()


