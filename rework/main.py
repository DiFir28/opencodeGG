import numpy as np
import time
import math
import json
import threading
import geometry as gm
import Camera
import cv2
from Shared import therds_stop, hsv_frame_queue


Camera.theard.start()

time.sleep(3)
while True:
    frame = hsv_frame_queue.get()
    cv2.imshow("Cap",frame)
    time.sleep(1)
    if cv2.waitKey(5) == 27:
                break
therds_stop.set()
Camera.theard.join()

