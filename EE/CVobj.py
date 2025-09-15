import cv2
import numpy as np
from geometry import vec, point, sign, tup
from shared import therds_stop, process_stop, img_resolution
import math
import SharedArray as sa
import threading
import time
import json
from camera import current_frame, process
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


#receive = ser.readline().decode('utf-8')
#dt = time.time()*1000 - float(receive)

with open('cent.json', 'r', encoding='utf-8') as file:
     cent = json.load(file)
     img_cent = cent["cent"]

with open('borders.json', 'r', encoding='utf-8') as file:
     borders = json.load(file)


class CVobj:
    def __init__(self, global_bound:tuple,name = "test", local_bound = None,mobility = True, shape = "ball", v_sect = True, color = ( 0, 200, 200) ):
        
        self.img_w, self.img_h = img_resolution
        self.center_point = point(img_cent[0] , img_cent[1] )   # + conf.center_dx, + conf.center_dy
        
        self.mod = mobility
        self.name = name
        self.sahpe = shape
        self.glob_bound = global_bound
        self.glob_bool_img = None
        self.glob_contour = None
        self.glob_point = point(0,0)
        self.draw_color = color
        
        self.img = None
        self.low_img = None
        
        
        self.sect_ = None
        self.ret = False
        self.sect_point = point(0,0)
        self.sect_dx, self.sect_dy = 0, 0
        
        self.loc_bound = local_bound
        if local_bound == None:
            self.loc_bound = global_bound
        self.loc_bool_img = None
        self.loc_contour = None
        self.loc_point = point(0,0)
        
        self.main_vec = vec()

        self.prev_t = time.time()
        self.fps = 0
        
        for name, value in globals().items():
            if value is self:
                self.name_ = name
        else:
            self.name_="33"
    
    def calcbool(self, simg, bound):
        simg = cv2.cvtColor(simg, cv2.COLOR_BGR2HSV )
        res = cv2.inRange(simg,tuple(bound[0]),tuple( bound[1]))
        '''
        for i in range(3,len(bound)):
            res += res + cv2.inRange(simg,bound[i][0], bound[i][1])'''
        res[res>255]=255                
        return res
    
    def cent_cont(self, cont):
        moment = cv2.moments(cont)
        area = moment['m00']
        if(area != 0):
            xm = moment['m01']
            ym =  moment['m10']
            y = int( xm/ area)
            x = int( ym/ area)
            return x , y
        else:
            
            print(self.name, "ZERO AREA")
            return tup(self.glob_point)
        
    def calccont(self, bimg, join = 0, min_val =0):
        all_contours, _ = cv2.findContours(bimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        '''
        max_area = 0
        max_contour = None
        for contour in all_contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour'''
        try:  
            eee = sorted(all_contours, key=cv2.contourArea, reverse=True)
            max_contour = eee[0]
            for i in range(min(join, len(eee)-1)):
                if (cv2.contourArea(eee[i+1]) >= min_val):
                    max_contour = np.vstack((max_contour, eee[i+1]))
            '''
            if join >0:
                max_contour = np.vstack((eee[0], eee[1]))
            else:
                max_contour = eee[0]'''
            max_area = cv2.contourArea(max_contour)
            return 1, max_contour, max_area
        except:
            return 0, self.glob_contour,0
    
    
    
    def calcsection(self, contour, area):        
        if area <= 2:
            M = cv2.moments(contour)
            
            if M["m00"] != 0: 
                c_x = int(M["m10"] / M["m00"])
                c_y = int(M["m01"] / M["m00"])
            else:
                return 0, 0, self.img_w, self.img_h
        #else:
        #        return 0, 0, img_w, img_h
        x, y, w, h = cv2.boundingRect(contour)
        x*=4
        y*=4
        w*=4
        h*=4
        
        return max(x - 0.5 * w,0), max(y - 0.5 * h,0), min(x + 1.5 * w, self.img_w-1), min(y + 1.5 * h, self.img_h-1)
        
        #(center_x, center_y), radius = cv2.minEnclosingCircle(contour)
        
        #rotated_rect = cv2.minAreaRect(self.glob_contour)
        #box_points = np.int0(cv2.boxPoints(rotated_rect))  # Получаем координаты углов прямоуг
        #cropped_image = image[y1:y2, x1:x2]
    
    def calcang(self):
        
        #try:
            try:
                self.loc_bool_img = self.calcbool(self.sect, self.loc_bound)
                ret,self.loc_contour, a =  self.calccont(self.loc_bool_img,min_val = 10)
                #cv2.drawContours(self.sect, [self.loc_contour], 0, self.draw_color, 3)
            except:
                self.loc_bool_img = self.calcbool(self.sect, self.glob_bound)
                ret,self.loc_contour, a =  self.calccont(self.loc_bool_img, min_val = 10)
                #cv2.drawContours(self.sect, [self.loc_contour], 0, (255, 0, 0), 3)
        
        
            xx, yy = self.cent_cont(self.loc_contour)
            self.loc_point = point(xx, yy)
            self.glob_point = self.loc_point + self.sect_point
            #cv2.line(self.img, tup(self.center_point), (self.glob_point.x, self.glob_point.y), self.draw_color, 3)
            #cv2.circle(self.img, tup(self.glob_point), 0, (255, 0, 0), 3)
            self.convert_glob_point =  point(0,0)
            self.convert_glob_point.x = (self.center_point.y - self.glob_point.y)
            self.convert_glob_point.y = (self.center_point.x - self.glob_point.x)
            
            
            self.main_vec = vec(endi = self.convert_glob_point)
            
            #cv2.circle(img, tup(center_point), 5, (250,255,100), 2)
            #cv2.circle(img, (self.glob_point.x, self.glob_point.y), 10, self.draw_color, 2)
        #except:
            #print("None ball")
        
       
        
    
    
    @property
    def sect(self, iimg = None):
        return self.sect_ 
    
    @sect.setter  
    def sect(self, iimg):
        self.img = iimg
        self.low_img = cv2.resize(iimg, (int(img_resolution[0]/4), int(img_resolution[1]/4)))
        self.glob_bool_img = self.calcbool(self.low_img, self.glob_bound)
        #cv2.imshow(f"{self.name} bool_img",self.glob_bool_img)
        
        ret,self.glob_contour , self.glob_contour_area = self.calccont(self.glob_bool_img, 0, 5)
        x1, y1, x2, y2 = map(int, self.calcsection(self.glob_contour, self.glob_contour_area))
        self.sect_point = point(x1,y1)
        self.sect_= iimg[y1:y2,x1:x2].copy()
        self.fps = 1/(time.time() - self.prev_t)
        self.prev_t=time.time()
        
        '''
        try:
            
            #cv2.imshow(f"{self.name} sect",self.sect_)
        except:
            print(x1, y1, x2, y2)
            print("None of sect")
            '''
            
    
        
             
def fieldimg(img, img_center):
    
    #cv2.circle(img, img_center, 5, (255,255,255), 1)
    #cv2.circle(img, img_center, 338, (255,255,255), 200)
    #cv2.circle(img, img_center, 50, (255,255,255), -1)
    
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    field_parts = cv2.inRange(hsv_img, (40, 140, 60), (85, 255, 255))
    field_parts_cont, _ = cv2.findContours(field_parts, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contour_areas = [(contour, cv2.contourArea(contour)) for contour in field_parts_cont]
    sorted_contours = sorted(contour_areas, key=lambda x: x[1], reverse=True)
    main_parts_field = []
    for i in range(min(2,len(sorted_contours))):
        #cv2.drawContours(img, sorted_contours[i][0], -1, (0, 255, 0), 3)
        main_parts_field.append(sorted_contours[i][0])

    main_field_points = np.vstack([cnt for cnt in main_parts_field])

    field_hull = cv2.convexHull(main_field_points)
    mask = np.zeros_like(img[:,:,0])    
    cv2.drawContours(mask, [field_hull], -1, 255, -1)
    
    img = cv2.bitwise_and(img, img, mask=mask)
    return img

def out_check(img, color):
    
    #cv2.circle(img, img_center, 5, (255,255,255), 1)
    #cv2.circle(img, img_center, 338, (255,255,255), 200)
    #cv2.circle(img, img_center, 50, (255,255,255), -1)
#     cv2.circle(img, (img_cent[0], img_cent[1]),  170, (0, 0, 0), -1)
    
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    
    field_parts = cv2.inRange(hsv_img,  tuple(color[0]), tuple(color[1]))
    # cv2.imshow("bb00l", field_parts)
    field_parts_cont, _ = cv2.findContours(field_parts, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # contour_areas = [(contour, cv2.contourArea(contour)) for contour in field_parts_cont]
    # sorted_contours = sorted(contour_areas, key=lambda x: x[1], reverse=True)
    closest_cont = None
    closest_dir = 400
    for i in field_parts_cont:
        moment = cv2.moments(i)
        area = moment['m00']
        if(area != 0):
            xm = moment['m01']
            ym =  moment['m10']
            y = int( xm/ area)
            x = int( ym/ area)
            
        else:
            continue
        out = vec(begi = point(img_cent[0],img_cent[1] ), endi = point(x, y))

        if out.ang == None or out.leng == None:
            continue
        if closest_dir > out.leng:
            closest_cont = out.copy()
            closest_dir = out.leng
            
        #cv2.drawContours(img, sorted_contours[i][0], -1, (0, 255, 0), 3)
    try:
        # print(closest_cont.ang, closest_dir)
        return vec(ang = closest_cont.ang, leng = closest_dir)
    except:
        # print(0,0)
        return vec(ang = 0, leng = -1)
    # return vec(ang = closest_cont.ang, leng = closest_dir)

def CVobj_threads(trg_obj: CVobj):
    print(trg_obj.name, "start")    
    time.sleep(1)
    while not(therds_stop.is_set()):
        trg_obj.sect = current_frame.copy()
        with threading.Lock():
            trg_obj.calcang()
        #time.sleep(0.01)
 
    print(trg_obj.name, "end")
    # not(stop_therds.is_set()):
        # cvobj.sect = input_frame.copy()
        # with threading.Lock():
        #     cvobj.calcang()
        # cv2.imshow(f"{cvobj.name} input", cvobj.img)
        
        #cv2.imshow("33", input_frame.copy())
        ##


if  __name__ == "__main__":

    try:
        process.start()
        while True:
            
           # CVobj_threads(ball)
            fr = current_frame.copy()
            #cv2.circle(fr, (img_cent[0], img_cent[1]),  170, (0, 0, 0), -1)
            cv2.imshow("fr", fr)
            a = out_check(fr, borders["yellow"]["glob"])
            try:
                print(a)
            except:
                print("lol")
            
            ch = cv2.waitKey(5)
            if ch == 27:
                break
        
    except KeyboardInterrupt:
        print("\n Break")
    finally:
        therds_stop.set()
        process_stop.set()
        time.sleep(0.1)
        cv2.destroyAllWindows()
        print("stop")
       


