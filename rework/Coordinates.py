import subprocess
import time
from Shared import coords, therds_stop
import threading
from math import *
from geometry import sign, rot
import SArduino
import json

import select
import sys

with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

field_valid_size=json["field_valid_size"]


def non_block_readline(pipe, timeout=0.0):
    r, _, _ = select.select([pipe], [], [], timeout)
    if r:
        return pipe.readline()
    return None


def ld06_data():
    global coords
    proc = subprocess.Popen(
        ["/home/pi/Desktop/ld06-master/build/ld06"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1
    )    
    time.sleep(5)
    prev_ang = 0
    try:

        while not(therds_stop.is_set()):
            try:
                response = non_block_readline(proc.stdout)

                if response is None:
                    continue
                # print(response)
                if len(response.split())!=5:
                    continue


            
                y, x, angr, wr, hr = response.split()
                wr = float(wr)
                hr = float(hr)
                w = min(wr, hr)/10
                h = max(wr, hr)/10
                # if (abs(h-field_valid_size[0])+abs(w-field_valid_size[1])) > 50:
                    
                #     with threading.Lock():
                #         coords[3] = False
                #     continue
                # ang =float(angr)
                # if w<h:
                #     ang-=3.1415926/2
                # if abs(ang-prev_ang) > 3:
                #     ang-=sign(ang-prev_ang)*3.1415926
                x = float(x)
                y = float(y)
                gyro = SArduino.gyro
                x,y=rot((x,y), gyro)
                # # print(round(ang,3), round(float(angr),3),(w>h))
                with threading.Lock():
                    coords[:] = [round(x/10), round(y/10), gyro,True]
                # print(coords)
                # prev_ang=ang

            except Exception as e:
              print(f"Лидар {e}")
                

        
    except Exception as e:
        print(f"Ошибка чтения: {e}")
    except KeyboardInterrupt:
        None


    finally:
        proc.terminate()
        print("GG")



thread = threading.Thread(target=ld06_data)
thread.daemon = False

if  __name__ == "__main__":
    SArduino.thread.start()
    thread.start()

    try:
        while True:
            # print(SArduino.gyro)
            print(coords)
            time.sleep(0.1)
            pass
        
    except KeyboardInterrupt:
        therds_stop.set()
        print("\nПрограмма завершена")
