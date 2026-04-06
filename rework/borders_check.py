import cv2
import numpy as np
from picamera2 import Picamera2
import json
import threading
import geometry as gm
from Shared import therds_stop, hsv_frame_queue
import Camera


if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow( "result" ) # создаем главное окно
cv2.namedWindow( "settings" ) # создаем окно настроек

Camera.theard.start()
# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]

while True:
    hsv = hsv_frame_queue.get()
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    # формируем начальный и конечный цвет фильтра
    h_min = (h1, s1, v1)
    h_max =(h2, s2, v2)
    

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('result', cv2.resize(thresh, (440,440))) 
    cv2.imshow('raw', cv2.cvtColor(cv2.resize(hsv, (440,440)), cv2.COLOR_HSV2BGR))
    cv2.imshow('ball', cv2.cvtColor(hsv[820:860,952:992], cv2.COLOR_HSV2BGR))
    ball_frame=hsv[820:860,952:992]
    print("Mean H:", np.sum(hsv[820:860, 952:992, 0]))

 
    ch = cv2.waitKey(5)
    
    if ch == 27:
        break

print(h_min,h_max)
therds_stop.set()
Camera.theard.join()
cv2.destroyAllWindows()
