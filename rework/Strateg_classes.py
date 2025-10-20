from geometry import *

class STobj(self):
    pos = point(0,0)
    vel = vec(beg = pos, ang = 0, len = 0)


def angTo(STobj: a, STobj: b):
    c = vec(beg = a.pos, end = b.pos)
    return c.ang

def disTo(STobj: a, STobj: b):
    c = vec(beg = a.pos, end = b.pos)
    return c.leng



# def act():s



if __name__ == "__main__":

      
