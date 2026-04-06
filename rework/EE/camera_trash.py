import time
import threading
from multiprocessing import Process, shared_memory

from picamera2 import Picamera2
import cv2
import numpy as np
from shared import stop_therds, cap_resolution

img = None
fps = 0

cap = Picamera2()

config = cap.create_preview_configuration(
    main={
        "format": "BGR888",
        "size": cap_resolution,
    },
    raw={
        "size": cap.sensor_resolution,
    },
    
    sensor={"output_size": cap_resolution}
)


cap.configure(config)

cap.set_controls({
    "ExposureTime": 10000,  
    "AeEnable": False,    
    # "AwbEnable": False, 
})

cap.start()
frame =  cv2.cvtColor(cap.capture_array(), cv2.COLOR_RGB2BGR)
seter_frame = frame

try:
    shared_frame_mem = shared_memory.SharedMemory(name = "act_frame", create = False, size=seter_frame.nbytes)
except:
    shared_frame_mem = shared_memory.SharedMemory(name = "act_frame", create = True, size=seter_frame.nbytes)

frame = np.ndarray(seter_frame.shape, dtype = seter_frame.dtype, buffer = shared_frame_mem.buf)

def update(mem, seter_arr):
    
    prev_t =0.0
    shared_frame = np.ndarray(seter_arr.shape, dtype = seter_arr.dtype, buffer = mem.buf)
    print("Cap start")
    while not(stop_therds.is_set()):        
       
        frame =  cv2.cvtColor(cap.capture_array(), cv2.COLOR_RGB2BGR)
        np.copyto(shared_frame, frame)
        fps = 1/(time.time()-prev_t)
        prev_t = time.time()
    cap.stop()
    print("Cap free")


camera_thread = Process(target=update, args = (shared_frame_mem, seter_frame))


if  __name__ == "__main__":

    try:
        camera_thread.start()
        while True:
            cur_frame = frame.copy()

            print(fps)
            cv2.imshow("Camera Frame", cv2.resize(cur_frame, (800,600)))
            ch = cv2.waitKey(5)
            if ch == 27:
                break
        
    except KeyboardInterrupt:
        print("\n Break")
    finally:
        stop_therds.set()
        time.sleep(0.1)
        cv2.destroyAllWindows()
        print("stop")
        


