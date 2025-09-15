from shared import process_stop
import camera
import numpy as np
import json
import time
import cv2

# borders = {
#     "orange": {"loc": [] , "glob":[]},
#     "yellow": {"loc": [] , "glob":[]},
#     "green" : {"loc": [] , "glob":[]},
#     "blue"  : {"loc": [] , "glob":[]},
#     "white" : {"loc": [] , "glob":[]},
# }


camera.process.start()

start_t = time.time()

with open('borders.json', 'r', encoding='utf-8') as file:
    borders = json.load(file)
    
keys = ["orange", "yellow", "green", "blue", "white"]
access = ["glob", "loc"]

if __name__ == '__main__':
    def nothing(*arg):
        pass
cv2.namedWindow( "img" )
cv2.namedWindow( "result" ) # создаем главное окно
cv2.namedWindow( "settings" ) # создаем окно настроек


#img = cv2.imread("baner.jpg")
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
cv2.createTrackbar('key: o-y-g-b', 'settings', 0, 3, nothing)
cv2.createTrackbar('access: glob-loc', 'settings', 0, 1, nothing)
crange = [0,0,0, 0,0,0]

img_h, img_w, chan = 1640, 1232, 3
while True:
    
    #cv2.putText(img, f"FPS: {int(fps)}", (img_w-100, img_h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    
    
    '''ch = cv2.waitKey(5)
    if ch == 49:
        _, img = cap.read()'''
    
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #img = cv2.imread('/home/pi/Desktop/anemo/korea.png', cv2.IMREAD_COLOR)
    #img = cv2.resize(img, (640, 480))
    '''gamma = 2 # >1 — затемнение, <1 — осветление
    lookup_table = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)], dtype=np.uint8)
    img = cv2.LUT(img, lookup_table)
    
    alpha = 0.8  # Контрастность (1.0 - оригинал, >1 - увеличить)
    beta = 10     # Яркость (0 - без изменений)
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    '''
    img =  camera.current_frame.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings') # формируем начальный и конечный цвет фильтра
    act_key = keys[cv2.getTrackbarPos('key: o-y-g-b', 'settings')]
    act_access = access[cv2.getTrackbarPos('access: glob-loc', 'settings')]
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8) # накладываем фильтр на кадр в модели

    thresh = cv2.inRange(hsv, (h1, s1, v1), (h2, s2, v2))
    res = cv2.bitwise_and(img, img, mask=thresh)
    '''contours2 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2 = sorted(contours2, key=cv2.contourArea, reverse=True)
    if (len(contours2)):
        print(cv2.contourArea(contours2[0]))'''
    cv2.imshow("result",  cv2.resize(res, None, fx=0.5, fy=0.5) )
    cv2.imshow("bool",  cv2.resize(thresh, None, fx=0.5, fy=0.5) )
    cv2.imshow("img",  cv2.resize(img, None, fx=0.5, fy=0.5) )
    print(img_w)
    
    ch = cv2.waitKey(5)
    
    if ch == 115 or ch == 217:    
        borders[act_key][act_access] = [[h1, s1, v1], [h2, s2, v2]]
        print(f"set to {act_key}, {act_access}")
    
    
    if ch == 27:
        print(f'({h1}, {s1}, {v1}), ({h2}, {s2}, {v2})')
        break
#cap.release()
cv2.destroyAllWindows()

with open('borders.json', 'w', encoding='utf-8') as file:
    json.dump(borders, file, ensure_ascii=False, indent=4)
 
process_stop.set()