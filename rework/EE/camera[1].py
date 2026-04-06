from multiprocessing import Process, Event, shared_memory
import time
import numpy as np
from picamera2 import Picamera2
import cv2
import json
from shared import img_resolution ,cap_resolution, process_stop

with open('cent.json', 'r', encoding='utf-8') as file:
     cent = json.load(file)
     img_cent = cent["cent"]


frame_shape = (img_resolution[1], img_resolution[0], 3) 
frame_dtype = np.uint8

try:
    shared_mem = shared_memory.SharedMemory(name="cur_frm", create=True, size=int(np.prod(frame_shape)) * np.dtype(frame_dtype).itemsize)
except:
    shared_mem = shared_memory.SharedMemory(name = "cur_frm")
    print("mem err")
current_frame = np.ndarray(frame_shape, dtype=frame_dtype, buffer=shared_mem.buf)


def update(stop_event):

    try:

        print("Camera starting...", end = "")
        cap = Picamera2()
        config = cap.create_preview_configuration(
            main={"format": "BGR888", "size": cap_resolution,},
            raw={"size": cap.sensor_resolution,},            
            sensor={"output_size": cap_resolution}
        )
        cap.configure(config)
        cap.set_controls({
            "ExposureTime": 15000,  
            "AeEnable": False,    
            # "AwbEnable": False, 
        })
        cap.start()
        print("Done")


        print("Shared_memory starting...", end = "")
        shared_mem = shared_memory.SharedMemory(name = "cur_frm")
        frame_shape = (img_resolution[1], img_resolution[0], 3)
        frame_dtype = np.uint8
        shared_frame = np.ndarray(frame_shape, dtype=frame_dtype, buffer=shared_mem.buf)
        print("Done")

        prev_t = time.time()
        fps = 0
        cut =int( ( cap_resolution[0] - cap_resolution[1] )/2)

        while (not stop_event.is_set()):

            current_frame =  (cv2.cvtColor(cap.capture_array(), cv2.COLOR_RGB2BGR))[:,cut:(cut+cap_resolution[1])] 
            #SDSScv2.circle(current_frame, (img_cent[0], img_cent[1]),  550, (0, 0, 0), 260)
            np.copyto(shared_frame, current_frame)

            # fps = 1/(time.time()-prev_t)
            # prev_t = time.time()
            # print("FPS", fps)

    except KeyboardInterrupt:
        print("Break")  
    finally:
        print("Camera process close...", end = "")
        shared_mem.close()
        shared_mem.unlink()
        cap.stop()
        cap.close()
        print("Done")
    

process = Process(target = update, args = (process_stop,), daemon = False)



print("Start")
if __name__ == "__main__":
    process.start()
    try:
        while True:
            new_arr = current_frame.copy() 
            cv2.imshow("Camera Frame", cv2.resize(new_arr, (600,600)))
            time.sleep(0.1)
            ch = cv2.waitKey(5)
            if ch == 27:
                    break

    except KeyboardInterrupt:
        print("Break")

    finally:    
        print("Ending...")
        time.sleep(1.5)
        process_stop.set()
        process.join()    
        shared_mem.close()
        print("End")
    