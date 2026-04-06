import time
import threading
import json
import cv2
import camera
import SharedArray as sa
from shared import therds_stop, process_stop, cap_resolution
from CVobj import CVobj, fieldimg, CVobj_threads, out_check
from geometry import vec, point, sign, tup, between
import numpy as np
import theard_serial
import math

with open('borders.json', 'r', encoding='utf-8') as file:
     borders = json.load(file)

with open('cent.json', 'r', encoding='utf-8') as file:
     cent = json.load(file)
     img_cent = cent["cent"]

camera.process.start()
time.sleep(1)

ball = CVobj(global_bound =  borders["orange"]["glob"], local_bound =  borders["orange"]["loc"], name = "Ball" )
blue_goal = CVobj(global_bound =  borders["blue"]["glob"], local_bound =  borders["blue"]["loc"], name = "Blue goal" )
yellow_goal = CVobj(global_bound =  borders["yellow"]["glob"], local_bound =  borders["yellow"]["loc"], name = "Yellow goal" )

ball_thread  = threading.Thread(target = CVobj_threads, args = (ball,),daemon = False )
blue_thread  = threading.Thread(target = CVobj_threads, args = (blue_goal,),daemon = False )
yellow_thread  = threading.Thread(target = CVobj_threads, args = (yellow_goal,),daemon = False )
ball_thread.start()
blue_thread.start()
yellow_thread.start()

read_thread = threading.Thread(target=theard_serial.read_from_arduino)
read_thread.daemon = True
read_thread.start()


def convert_px_to_cm(px :float):
    return round( 217/(-0.04563*px + 18.8999) - 1.66885)


gyro = 0
pos = [0,0,0]

vec_from_blue = vec(begi = point(0, 105))
vec_from_yellow = vec(begi = point(0, -105))

vec_in_blue = vec(endi = point(0, 90))
vec_in_yellow = vec(endi = point(0, -90))

ball_get_t = time.time()
ball_ret = False
time_last_state = time.time()

lin_dir, lin_vel, main_dir, drb_p, rot_const = 0, 0, 0, 0, 0

main_state = 1  

'''
0 - fast to
1 - slow to
2 - stop whith

3 - turn opp goal
4 - turn to goal
'''

if  __name__ == "__main__":  
    try:
        
        while True:
            fr = camera.current_frame.copy()
            try:
                gyro = float(theard_serial.data)
            except:
                print("OG ", end = "")

            vec_to_line = out_check(fr, borders["green"]["glob"])

            vec_from_blue.ang =  -blue_goal.main_vec.ang + math.pi + gyro
            vec_from_blue.leng =  convert_px_to_cm(blue_goal.main_vec.leng)   

            vec_from_yellow.ang =  -yellow_goal.main_vec.ang + math.pi + gyro
            vec_from_yellow.leng =  convert_px_to_cm(yellow_goal.main_vec.leng) 


            if ball.main_vec.leng < 143:
                ball_ret = True                
            else:
                ball_ret = False
                ball_get_t = time.time()

            # if ball.main_vec.leng > 250:
            #     main_state = 0
            # elif main_state == 0:
            #     main_state = 1
                        
        



            
            if ball.main_vec.leng > 250:
                lin_dir, lin_vel = int(round(gyro - ball.main_vec.ang,3)*1000), 4000 
                main_dir, rot_const = lin_dir, 10000
                drb_p = 0

            elif main_state == 1:
                lin_dir, lin_vel = int(round(gyro - ball.main_vec.ang,3)*1000), 1000 
                main_dir, rot_const = lin_dir, 10000
                drb_p = 230
                if ball_ret:
                    main_state = 2
                    time_last_state = time.time()

            elif main_state == 2 :
                lin_dir, lin_vel = int(round(gyro - ball.main_vec.ang,3)*1000), 0 
                main_dir, rot_const = lin_dir, 7000
                drb_p = 300
                if time.time() - time_last_state > 1:
                    main_state = 3
                    time_last_state = time.time()
                if not ball_ret:
                    main_state = 1


                

            elif main_state == 3:
                lin_dir, lin_vel = 0, 0 
                main_dir, rot_const = int(round(gyro - blue_goal.main_vec.ang - math.pi,3)*1000), 500
                drb_p = 300
                if time.time() - time_last_state > 2:
                    if ball_ret:
                        main_state = 4
                        time_last_state = time.time()
                    else:
                        main_state = 1

            elif main_state == 4:
                lin_dir, lin_vel = int(round(gyro - blue_goal.main_vec.ang,3)*1000), 0 
                main_dir, rot_const = lin_dir, 5000
                drb_p = 150
                if time.time() - time_last_state > 2:
                    main_state = 1

            # if time.time()-time_last_state > 10:
            #     main_state = 0

            


            

                








            
            cv2.line(fr, tup(ball.center_point), tup(ball.glob_point), (0,100,255), 2)
            cv2.line(fr, tup(blue_goal.center_point), tup(blue_goal.glob_point), (255,0,0), 2)
            cv2.line(fr, tup(yellow_goal.center_point), tup(yellow_goal.glob_point), (0,200,255), 2)
            #theard_serial.write_to_arduino(f',{0},{0},{0},{0},{10},')
            a = vec(begi = point(0,90), ang = 240/180*math.pi, leng = 50)
            #print(f"{gyro}   {vec_from_blue.end} ; {vec_from_yellow.end} ; {convert_px_to_cm(blue_goal.main_vec.leng) } ; {convert_px_to_cm(yellow_goal.main_vec.leng*1) } ; {vec_from_blue.ang * 180 / math.pi} ; {vec_from_yellow.ang * 180 / math.pi} a {a.end}")
            #print(ball.main_vec.ang, main_state,  round(time.time() - time_last_state, 3), convert_px_to_cm(vec_to_line.leng))

            print(gyro, lin_dir, round(vec_to_line.ang - gyro,3), round(abs(between(lin_dir/1000, (gyro - vec_to_line.ang))),3) , convert_px_to_cm(vec_to_line.leng), end = " ")

            if convert_px_to_cm(vec_to_line.leng) < 25 and abs(between(lin_dir/1000, (vec_to_line.ang - gyro))) < 1:
                lin_vel = 0
            if convert_px_to_cm(vec_to_line.leng) < 18:
                lin_vel = 500
                lin_dir = round(vec_to_line.ang - gyro   + math.pi,3)*1000

            

            print(lin_vel)
            #lin_vel = 0
            theard_serial.write_to_arduino(f',{lin_dir}, {lin_vel}, {main_dir}, {drb_p}, {rot_const},')
            #print(f',{lin_dir},{lin_spd},{front_dir},{0},{0},')

            
            #cv2.imshow("ww", fr )S
            #cv2.imshow("fr",  cv2.resize(fr, None, fx=0.2, fy=0.2) )
            # print(ball.main_vec.ang, blue_goal.main_vec.ang)
           
            time.sleep(0.001)
            ch = cv2.waitKey(5)
            if ch == 27:
                break
        
    except KeyboardInterrupt:
        print("\nПрограмма завершена")
    finally:
        print("Stoping")
        theard_serial.write_to_arduino(f',{0}, {0}, {0}, {0}, {0},')

        print("Ending...")
        process_stop.set()
        therds_stop.set()
        camera.process.join()
        
        time.sleep(0.1)
        cv2.destroyAllWindows()
        print("End")


