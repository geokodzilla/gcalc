#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math as m


class Point(object):

    """
    Klasa reprezntująca punkt w przestrzeni dwuwymiarowej
    """

    def __init__(self, number, x, y, d='0', id=None):
        self.number = number # numer punktu nie musi być unikatowy
        self.x = x
        self.y = y
        self.d = d
        self.id = id # unikatowy identyfikator obiektu na mapie

    def __str__(self):
        return "{} {} {} {}".format(self.number, str(self.x), str(self.y),
                                    str(self.d))

    def save(self):
        return "{} {} {} {}\n".format(self.number, str(round(self.x, 2)),
                                      str(round(self.y, 2)), str(self.d))

    def dist(self, p):
        """
        Metoda wyznaczjąca odległość pomiędzy dwoma punktami.
        :param p:
        :return:
        """
        dx = self.x - p.x
        dy = self.y - p.y
        self.d = round(m.sqrt(pow(dx, 2) + pow(dy, 2)), 2)

    def set_id(self, id):
        """
        Metoda ustawiająca identyfikator obiektu
        """
        self.id = id

        