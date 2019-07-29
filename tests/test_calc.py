# -*- coding: utf-8 -*-

import pytest
from calc import domiary, przeciecie, roznice
from point import Point

    
@pytest.mark.parametrize("dane,wsp", [
                                        ([5652236.89, 7566946.64, 5652251.95, 7566950.43, 3 ,2], [5652239.31, 7566949.31]),
                                        ([5652236.89, 7566946.64, 5652251.95, 7566950.43, 2 ,-3], [5652239.56, 7566944.22]),
                                        ([5652236.89, 7566946.64, 5652251.95, 7566950.43, -1 ,2], [5652235.43, 7566948.34])
])
def test_domiary(dane, wsp):
    sp_x, sp_y, ep_x, ep_y, odcieta, rzedna = dane
    sp = Point('1', sp_x, sp_y)
    ep = Point('2', ep_x, ep_y)
    res_p = domiary('3', sp, ep, odcieta, rzedna)
    assert res_p.x == wsp[0]
    assert res_p.y == wsp[1]
    
    
@pytest.mark.parametrize("dane,wsp", [
                                        ([5652236.89, 7566946.64, 5652251.95, 7566950.43,
                                          5652249.48, 7566942.02, 5652246.12, 7566954.80],[5652247.56, 7566949.33])
           
])
def test_przeciecie(dane, wsp):
    sp_x, sp_y, ep_x, ep_y, sp2_x, sp2_y, ep2_x, ep2_y = dane
    sp = Point('1', sp_x, sp_y)
    ep = Point('2', ep_x, ep_y)
    sp2 = Point('3', sp2_x, sp2_y)
    ep2 = Point('4', ep2_x, ep2_y)
    res_p = przeciecie('5', sp, ep, sp2, ep2)
    assert res_p.x == wsp[0]
    assert res_p.y == wsp[1]
    
    
@pytest.mark.parametrize("data,expected", [
                                        ([2, 100, 200], 1.0)
           
])
def test_roznice(data, expected):
    d, delta, odl = data
    assert roznice(d, delta, odl) == expected