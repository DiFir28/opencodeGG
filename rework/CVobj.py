import cv2
import numpy as np
from geometry import *
import math
import threading
import time
import json
from shared import therds_stop
from Camera_theard import raw_frame_hsv

def find_contour(hsv_img, bound, join = 1, min_area_join = 5):
        bool_img = cv2.inRange(hsv_img,tuple(bound[0]),tuple( bound[1]))
        '''
        for i in range(len(bound)):
            res += res + cv2.inRange(simg,bound[i][0], bound[i][1])
        res[res>255]=255  '''

        all_contours, _ = cv2.findContours(bool_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(all_contours) == 0:
            return 0, [], bool_img

        ranked_contours = sorted(all_contours, key=cv2.contourArea, reverse=True)

        res_contour = ranked_contours[0]
        for i in range( min(join, len(ranked_contours) - 1) ):
            if (cv2.contourArea(ranked_contours[i + 1]) >= min_area_join):
                res_contour = np.vstack( (res_contour, ranked_contours[i + 1]) )

        return len(ranked_contours), res_contour, bool_img


def cent_contour(cont):
        moment = cv2.moments(cont)
        area = moment['m00']
        if(area != 0):
            xm = moment['m01']
            ym =  moment['m10']
            y = int( xm/ area)
            x = int( ym/ area)
            return x, y
        else:
            return 0, 0




class CVobj:
    def __init__(self, name:str, img_resolution, global_bound:tuple,/, local_bound:tuple = None ,*, color:tuple = ( 0, 200, 200), div = 1, use_sect:bool = True ):
        
        self.name = name
        self.draw_color = color
        self.ret = False
        self.img = None
         
        self.div = div       
        self.resolution = img_resolution
        
        self.glob_bound = global_bound
        self.glob_contour = None         
        
        self.sect = None
        self.sect_point = point(0,0)
        
        self.loc_bound = local_bound
        if local_bound == None:
            self.loc_bound = global_bound

        self.loc_contour = None
        self.main_point = point(0,0)
        
        self.main_vec = vec(beg = point(img_resolution[0]/2, img_resolution[1]/2))

        self.prev_t = time.time()
        self.buf = 0
        self.fps = 0

    def calc_sect(self, img, contour):
        
        try:

            if cv2.contourArea(contour)<4:
                x,y = cent_contour(contour)
                w, h = 1,1
                x1, y1, x2, y2 = map(int, ( max(x - 0.5 * w, 0), max(y - 0.5 * h, 0), min(x + 1.5 * w, self.resolution[0] - 1), min(y + 1.5 * h, self.resolution[1] - 1)))
                return img[y1:y2,x1:x2].copy(), point(x1, y1), (x1, y1, x2, y2)

            x, y, w, h = cv2.boundingRect(contour)
            x *= self.div
            y *= self.div
            w *= self.div
            h *= self.div

           
            
            x1, y1, x2, y2 = map(int, ( max(x - 0.5 * w, 0), max(y - 0.5 * h, 0), min(x + 1.5 * w, self.resolution[0] - 1), min(y + 1.5 * h, self.resolution[1] - 1)))
            return img[y1:y2,x1:x2].copy(), point(x1, y1), (x1, y1, x2, y2)
        except:
            return img.copy(), point(0, 0), (0, 0, -1, -1)
            
    
    def main_calc(self, img, offset = True):
        
        n, self.glob_contour, _ = find_contour(img, self.glob_bound, join = 0)
        if n == 0:
            self.ret = False
            return 0
        self.sect, self.sect_point, _ = self.calc_sect(img, self.glob_contour)
        self.buf = self.sect
        n, self.loc_contour, _ = find_contour(self.sect, self.loc_bound)
        if n == 0:
            n, self.loc_contour, _ = find_contour(self.sect, self.glob_bound)
            offset = False
            if n == 0:
                self.ret = False
                return 
        self.ret = True
        x, y = map(int, cent_contour(self.loc_contour))
        self.main_point = point(x, y)
        self.main_point += self.sect_point
        self.main_vec.end = self.main_point
        
        


    # def theard(self):
    #     global raw_frame_hsv
    #     print(self.name, "start") 
    #     time.sleep(0.5)

    #     while not(therds_stop.is_set()):
    #         self.main_calc(raw_frame_hsv)
    #     print(trg_obj.name, "end")
                




if __name__ == "__main__":
    a = cv2.imread("test_brg.jpg")
   
    yellow = CVobj("Y", (1280, 960), ((0,100,100),( 20, 255, 255 )))
    yellow.ret = True

    n, yellow.glob_contour, _ = find_contour(cv2.cvtColor(a, cv2.COLOR_BGR2HSV), yellow.glob_bound)
            
    if n == 0:
        yellow.ret = False
        
        
    yellow.sect, yellow.sect_point, p = yellow.calc_sect(a, yellow.glob_contour)
    
    

    if yellow.ret:
        cv2.circle(a, (p[0], p[1]), 30, (200,100,0), -1)
        cv2.circle(a, (p[2], p[3]), 30, (200,100,0), -1)
        cv2.imshow("1", cv2.resize(a, (300,300)))

    k = 0
    while k != 27:
        k = cv2.waitKey(5)

    cv2.destroyAllWindows()



