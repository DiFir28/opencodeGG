from geometry import *
from Shared import therds_stop, hsv_frame_queue
import CVobj
import json
import Camera

with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

img_resolution = json["resolution"]["img"]

class STobj:
    def __init__(self, pos = point(0,0)):
        self.pos = pos
        self.vel = vec(beg = pos, ang = 0, leng = 0)


def angTo( a:STobj,  b:STobj):
    c = vec(beg = a.pos, end = b.pos)
    return c.ang

def disTo(a:STobj, b:STobj):
    c = vec(beg = a.pos, end = b.pos)
    return c.leng

def pix_to_cm(pix):
    return (0.000003744*pix**3-0.0036*pix**2+1.218*pix-110.4)

blue_goal = STobj(pos = point(0,-(json["dl_goals"])))
yellow_goal = STobj(pos = point(0,(json["dl_goals"])))

def cord_2goals():
    if CVobj.blue.ret and CVobj.yellow.ret:
        blue_goal.vec.leng = pix_to_cm(CVobj.blue.main_vec.leng)
        yellow_goal.vec.leng = pix_to_cm(CVobj.yellow.main_vec.leng)

        y_int = (blue_goal.vec.leng ** 2 - yellow_goal.vec.leng ** 2)/ (4*(json["dl_goals"]))
        x_int = math.sqrt( blue_goal.vec.leng ** 2 - (y_int + (json["dl_goals"]))**2  )
        print(x_int, y_int)

# def act():s

def horOut():
    return round(abs(math.sin(between(CVobj.blue.main_vec.ang, CVobj.yellow.main_vec.ang)))*CVobj.blue.main_vec.leng*CVobj.yellow.main_vec.leng/json["dl_goals"])

def closeToBlue():
    if CVobj.blue.main_vec.leng < 450:
        return 2
    elif CVobj.blue.main_vec.leng < 600:
        return 1
    return 0

def closeToYellow():
    if CVobj.yellow.main_vec.leng < 450:
        return 2
    elif CVobj.yellow.main_vec.leng < 600:
        return 1
    return 0


import cv2
import numpy as  np
import math

cage_n = 8
cage_space = 20
cage_w = 2

overall_size =  cage_n*(cage_space+cage_w)+cage_w
print(overall_size)
arr = np.zeros((overall_size,overall_size,3),np.int8)

for i in range(cage_n+2):
    cv2.rectangle(arr,(int(i*(cage_space+cage_w)),0), (int(cage_w+i*(cage_space+cage_w)),overall_size-1),(255,255,255),cage_w)
    cv2.rectangle(arr,(0,int(i*(cage_space+cage_w))), (overall_size-1,int(cage_w+i*(cage_space+cage_w))),(255,255,255),cage_w)

# print(np.shape(arr),arr)
# cv2.imshow("img",arr)
# cv2.imwrite("field.jpg",arr)

transpared_cent=(img_resolution[0]//2, img_resolution[1]//2)


def pix_conv(a):
    ro=math.sqrt((a[0]-transpared_cent[0])**2+(a[1]-transpared_cent[1])**2)
    if a[0]==transpared_cent[0]and a[1]==transpared_cent[1]:
        return(a)
    cos = (a[0]-transpared_cent[0])/ro
    sin = (a[1]-transpared_cent[1])/ro
    new_ro=pix_to_cm(ro)
    #print(ro,new_ro)
    return (int(cos*new_ro),int(sin*new_ro))

# transparet = np.zeros((500,500,3),np.int8)

def transform(img):
    global transpared_cent,arr
   
    for i in range(img_resolution[0]):
        print(i)
        for j in range(img_resolution[1]):
            new=pix_conv((i,j))
            #print((i,j),new)
            try:
                if not np.array_equal(arr[89+new[0]][89-new[1]],(0,0,0)):
                    cv2.line(transparet,(i,j), (i,j),(255,255,255),1)
            except:
                None
    return img





if __name__ == "__main__":

    Camera.theard.start()
    CVobj.theard.start()
    try:
        while True:
            if hsv_frame_queue.empty():
                continue
            frame = hsv_frame_queue.get()
            frame=transform(frame)
            print("WON")
            cv2.imshow("Frame", cv2.resize(frame, (600,600)))  
            if cv2.waitKey(5) == 27:
                break
            
            # print(CVobj.blue.main_vec.leng, CVobj.yellow.main_vec.leng, abs(math.sin(between(CVobj.blue.main_vec.ang, CVobj.yellow.main_vec.ang)))*CVobj.blue.main_vec.leng*CVobj.yellow.main_vec.leng/json["dl_goals"] )
    except:
        therds_stop.set()
        Camera.theard.join()