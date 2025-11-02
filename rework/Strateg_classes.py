from geometry import *
from Shared import therds_stop, hsv_frame_queue
import CVobj
import json
import Camera

with open('config.json', 'r', encoding='utf-8') as file:
     json = json.load(file)

class STobj:
    def __init__(self, pos = point(0,0)):
        self.pos = pos
        self.vel = vec(beg = pos, ang = 0, leng = 0)


def angTo( a:STobj,  b:STobj):
    c = vec(beg = a.pos, end = b.pos)
    return c.ang

def disTo(a:STobj, b:STobj):
    c = vec(beg = a.pos, end = b.pos)
    return c.leng

def pix_to_cm(pix):
    return (0.000003744*pix**3-0.0036*pix**2+1.218*pix-110.4)

blue_goal = STobj(pos = point(0,-(json["dl_goals"])))
yellow_goal = STobj(pos = point(0,(json["dl_goals"])))

def cord_2goals():
    if CVobj.blue.ret and CVobj.yellow.ret:
        blue_goal.vec.leng = pix_to_cm(CVobj.blue.main_vec.leng)
        yellow_goal.vec.leng = pix_to_cm(CVobj.yellow.main_vec.leng)

        y_int = (blue_goal.vec.leng ** 2 - yellow_goal.vec.leng ** 2)/ (4*(json["dl_goals"]))
        x_int = math.sqrt( blue_goal.vec.leng ** 2 - (y_int + (json["dl_goals"]))**2  )
        print(x_int, y_int)

# def act():s

def horOut():
    return round(abs(math.sin(between(CVobj.blue.main_vec.ang, CVobj.yellow.main_vec.ang)))*CVobj.blue.main_vec.leng*CVobj.yellow.main_vec.leng/json["dl_goals"])

def closeToBlue():
    if CVobj.blue.main_vec.leng < 450:
        return 2
    elif CVobj.blue.main_vec.leng < 600:
        return 1
    return 0

def closeToYellow():
    if CVobj.yellow.main_vec.leng < 450:
        return 2
    elif CVobj.yellow.main_vec.leng < 600:
        return 1
    return 0


if __name__ == "__main__":

    Camera.theard.start()
    CVobj.theard.start()
    try:
        while True:
            print(CVobj.blue.main_vec.leng, CVobj.yellow.main_vec.leng, abs(math.sin(between(CVobj.blue.main_vec.ang, CVobj.yellow.main_vec.ang)))*CVobj.blue.main_vec.leng*CVobj.yellow.main_vec.leng/json["dl_goals"] )
    except:
        therds_stop.set()
        Camera.theard.join()