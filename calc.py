# -*- coding: utf-8 -*-
import math as m
from point import Point

def roznice(d, delta, odl):
    return d * (delta/odl)
    
def domiary(numer, sp, ep, odcieta, rzedna):
    sp.dist(ep)
    
    dxa = roznice(odcieta, (ep.x-sp.x), sp.d)
    dya = roznice(odcieta, (ep.y-sp.y), sp.d)
    
    dxi = roznice(m.fabs(rzedna), (ep.y-sp.y), sp.d)
    dyi = roznice(m.fabs(rzedna), (ep.x-sp.x), sp.d)
    
    if rzedna >= 0:
        xN = sp.x + dxa - dxi
        yN = sp.y + dya + dyi
    else:
        xN = sp.x + dxa + dxi
        yN = sp.y + dya - dyi
    return Point(str(numer), round(xN, 2), round(yN, 2))

def przeciecie(numer, sp, ep, sp2, ep2):
    l = (ep.y - sp.y)/(ep.x - sp.x)
    m = (ep2.y - sp2.y)/(ep2.x - sp2.x)
    
    xN = (sp2.y - sp.y + (l * sp.x) - (m * sp2.x))/(l - m)
    yN = sp.y + l * (xN-sp.x)
    return Point(str(numer), round(xN, 2), round(yN, 2))
    
    


