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
import pygame

BASE_RES = 800, 600

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


class Utils:
    scaled_screen_rect = None

    @staticmethod
    def norm_cursor_pos():
        rect = Utils.scaled_screen_rect
        mx, my = pygame.mouse.get_pos()
        dx = mx - rect.left
        dy = my - rect.top
        mouse_norm_x = dx * BASE_RES[0] / rect.width
        mouse_norm_y = dy * BASE_RES[1] / rect.height

        if mouse_norm_x < 0:
            mouse_norm_x = 0
        if mouse_norm_x >= BASE_RES[0]:
            mouse_norm_x = BASE_RES[0] - 1
        if mouse_norm_y < 0:
            mouse_norm_y = 0
        if mouse_norm_y >= BASE_RES[1]:
            mouse_norm_y = BASE_RES[1] - 1
        return mouse_norm_x, mouse_norm_y

    @staticmethod
    def get_act_pos(pos):
        rect = Utils.scaled_screen_rect
        x, y = pos
        sx, sy = rect.left, rect.top
        act_x = sx + (x * rect.width / BASE_RES[0])
        act_y = sy + (y * rect.height / BASE_RES[1])

        return act_x, act_y

    @staticmethod
    def render_multiple_lines(text, surface, right_margin, pos, color, font):
        rect = surface.get_rect()
        bound = rect.right - right_margin
        x, y = pos
        space = font.size(' ')[0]

        words = [line.split() for line in text.split('\n')]
        for line in words:
            for word in line:
                word_surf = font.render(word, False, color)
                word_width, word_height = word_surf.get_size()
                if x + word_width > bound:
                    x = pos[0]
                    y += word_height + 5

                surface.blit(word_surf, (x, y))
                x += word_width + space

            x = pos[0]
            y += word_height + 3
