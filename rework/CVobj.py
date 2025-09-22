import cv2
import numpy as np
from geometry import vec, point, sign, tup
import math
import threading
import time
import json


with open('cent.json', 'r', encoding='utf-8') as file:
     cent = json.load(file)
     img_cent = cent["cent"]


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
        
        self.main_vec = vec(begi = point(img_resolution[0]/2, img_resolution[1]/2))

        self.prev_t = time.time()
        self.fps = 0
        
    def calc_sect(self, img, contour):

        if cv2.contourArea(contour)<4:
            x,y = cent_contour(contour)
            return max(x - 5, 0), max(y - 5, 0), min(x + 5, self.resolution[0] - 1), min(y + 5, self.resolution[1] - 1)

        x, y, w, h = cv2.boundingRect(contour)
        x *= self.div
        y *= self.div
        w *= self.div
        h *= self.div
        
        x1, y1, x2, y2 = map(int, max(x - 0.5 * w, 0), max(y - 0.5 * h, 0), min(x + 1.5 * w, self.resolution[0] - 1), min(y + 1.5 * h, self.resolution[1] - 1))
        return img[y1:y2,x1:x2].copy()

			def main_calc(self, img, offset = True):
				n, self.loc_contour, _ = self.findcontour(img, self.local_bound)
				if n == 0:
					_, self.loc_contour, _ = self.findcontour(img, self.glob_bound)
					offeset = False

				x, y = cent_contour(self.loc_contour)
				self.main_point = point(self.sect_point.x + x, self.sect_point.y + y)
				self.main_vec.end = point(self.main_point)
				


				



