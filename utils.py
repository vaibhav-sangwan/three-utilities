#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Three Utilities
# Copyright (C) 2024 Vaibhav Sangwan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Vaibhav Sangwan    sangwanvaibhav02@gmail.com

import math

def dist(start, end):
    return math.hypot(start[0] - end[0], start[1] - end[1])

def lineLineIntersect(P0, P1, Q0, Q1):
    dx = (P1[0] - P0[0]) * (Q1[1] - Q0[1])
    dy = (P1[1] - P0[1]) * (Q0[0] - Q1[0])
    d = dx + dy
    if d == 0:
        return None
    tx = (Q0[0] - P0[0]) * (Q1[1] - Q0[1])
    ty = (Q0[1] - P0[1]) * (Q0[0] - Q1[0])
    t = (tx + ty) / d
    ux = (Q0[0] - P0[0]) * (P1[1] - P0[1])
    uy = (Q0[1] - P0[1]) * (P0[0] - P1[0])
    u = (ux + uy) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return round(P1[0] * t + P0[0] * (1 - t)), round(
            P1[1] * t + P0[1] * (1 - t)
        )
    return None

def segment_intersect(line1, line2):
    intersection_pt = lineLineIntersect(line1[0],
                                             line1[1],
                                             line2[0],
                                             line2[1])
    if not intersection_pt:
        return None
    minm = min(line1[0][0], line1[1][0])
    maxm = max(line1[0][0], line1[1][0])
    if intersection_pt[0] < minm or intersection_pt[0] > maxm:
        return None
    if intersection_pt[0] < minm or intersection_pt[0] > maxm:
        return None
    return intersection_pt