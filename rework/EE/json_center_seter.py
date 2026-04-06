from shared import process_stop, img_resolution
import camera
import numpy as np
import json
import time
import cv2

img_cent = {
    "cent": (0,0),
}


camera.process.start()

start_t = time.time()

# with open('borders.json', 'r', encoding='utf-8') as file:
#     borders = json.load(file)
    


if __name__ == '__main__':
    def nothing(*arg):
        pass
cv2.namedWindow( "img" )
cv2.namedWindow( "settings" ) # создаем окно настроек


#img = cv2.imread("baner.jpg")
cv2.createTrackbar('x', 'settings', 0, 150, nothing)
cv2.createTrackbar('y', 'settings', 0, 150, nothing)
cv2.createTrackbar('r', 'settings', 1, 1000, nothing)

crange = [0,0,0, 0,0,0]

img_h, img_w, chan = 1232, 1232, 3
while True:
    img =  camera.current_frame.copy()
    d_x = cv2.getTrackbarPos('x', 'settings')
    d_y = cv2.getTrackbarPos('y', 'settings')
    d_r = cv2.getTrackbarPos('r', 'settings')
    cv2.circle(img, (int(img_resolution[1]/2 + d_y-75), int(img_resolution[0]/2 + d_x - 75)),  d_r, (0, 0, 255), 2)
    cv2.imshow("img",  img )
    print(img_w)
    
    ch = cv2.waitKey(5)
    
    if ch == 115 or ch == 217:    
        img_cent["cent"] = (int(img_resolution[1]/2 + d_y-75), int(img_resolution[0]/2 + d_x - 75))
        print(f"set to")
    
    
    if ch == 27:
        
        break
#cap.release()
cv2.destroyAllWindows()

with open('cent.json', 'w', encoding='utf-8') as file:
    json.dump(img_cent, file, ensure_ascii=False, indent=4)
 
process_stop.set()