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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sugar3.graphics.style import GRID_CELL_SIZE

import math
from functools import cmp_to_key

import pygame
pygame.init()
from home import Home
from utility import Utility

INS_FONT = pygame.font.SysFont('ubuntumono', 18, bold=True)
ERROR_FONT = pygame.font.SysFont('ubuntumono', 24, bold=True)
INSTRUCTIONS = ["R - Restart", "S - Stop line"]

class ThreeUtilities:
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption('Three Utilities')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        self.screen = pygame.display.get_surface()
        if not self.screen:
            self.screen = pygame.display.set_mode((800, 600))
        w, h = self.screen.get_width(), self.screen.get_height()

        self.water = Utility(w/2 - 200, h/2 - 100, "water", "blue")
        self.elec = Utility(w/2, h/2 - 100, "electricity", "red")
        self.gas = Utility(w/2 + 200, h/2 - 100, "gas", "green")
        self.utilities = [self.water, self.elec, self.gas]
        self.homes = [Home(w/2 - 200, h/2 + 100, self.utilities), Home(w/2, h/2 + 100, self.utilities), Home(w/2 + 200, h/2 + 100, self.utilities)]
    
        self.originate = None
        self.lines = []

        self.err_message = None
        self.collision_point = None
    
    def draw(self):
        self.screen.fill("white")

        for i in range(len(self.lines)):
            line = self.lines[i]
            for j in range(1, len(line) - 1):
                pygame.draw.line(self.screen, line[0].color, line[j], line[j + 1], 3)
            if (i == len(self.lines) - 1) and self.originate:
                pygame.draw.line(self.screen, line[0].color, line[-1], pygame.mouse.get_pos(), 3)
            

        for home in self.homes:
            home.update(self.py_events)
            self.screen.blit(home.image, (home.rect.left - 9, home.rect.top - 16))
            cxs = [home.rect.centerx - 16, home.rect.centerx, home.rect.centerx + 16]
            i = 0
            for util in home.connected:
                pygame.draw.circle(self.screen, util.color, (cxs[i], home.rect.bottom + 15), 5, 2 if not home.connected[util] else 0)
                i += 1

        for util in self.utilities:
            util.update(self.py_events)
            self.screen.blit(util.image, util.rect)
        
        if self.collision_point:
            pygame.draw.circle(self.screen, "red", self.collision_point, 5)
            error = ERROR_FONT.render(self.err_message, False, "red")
            error_rect = error.get_rect(center = (self.screen.get_width()/2, self.screen.get_height() - 30))
            self.screen.blit(error, error_rect)
        
        top = 10
        for instruction in INSTRUCTIONS:
            inst = INS_FONT.render(instruction, False, "black")
            inst_rect = inst.get_rect(topleft = (10, top))
            top += 20
            self.screen.blit(inst, inst_rect)
        
        
    
    def lineLineIntersect(self, P0, P1, Q0, Q1):  
        d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
        if d == 0:
            return None
        t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
        u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
        if 0 <= t <= 1 and 0 <= u <= 1:
            return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))
        return None

    def segment_intersect(self, line1, line2) :
        intersection_pt = self.lineLineIntersect(line1[0], line1[1], line2[0], line2[1])

        if not intersection_pt:
            return None
    
        if intersection_pt[0] < min(line1[0][0], line1[1][0]) or intersection_pt[0] > max(line1[0][0], line1[1][0]):
            return None
        if intersection_pt[0] < min(line2[0][0], line2[1][0]) or intersection_pt[0] > max(line2[0][0], line2[1][0]):
            return None

        return intersection_pt    

    def lines_collide(self, ts, te, os, oe, originating, terminating):
        intersect_point = self.segment_intersect((ts, te), (os, oe))
        if terminating and terminating.connected[self.originate]: # when the line is connecting a supply to already connected house
            self.err_message = "Already Connected"
            self.collision_point = terminating.rect.center
            return True
        if (ts, te) == (os, oe) or (ts, te) == (oe, os): # when the lines are coincident
            self.err_message = "Collision"
            self.collision_point = te
            return True
        if not intersect_point:
            return False
        if intersect_point == ts and originating:
            return False
        if intersect_point == te and terminating:
            return False
        
        self.collision_point = intersect_point
        self.err_message = "Collision"
        return True
        
    
    def check_collision(self, start, end, startNode, endNode):
        for i in range(len(self.lines)):
            line = self.lines[i]
            for j in range(1, len(line) - 1):
                if i == len(self.lines) - 1 and j == len(line) - 2:
                    continue
                if self.lines_collide(start, end, line[j], line[j + 1], startNode, endNode):
                    return True
        return False

    def dist(self, start, end):
        return math.hypot(start[0]-end[0], start[1]-end[1])
    
    def draw_line(self, start, end):
        startNode = None
        endNode = None

        for home in self.homes:
            if start == home.rect.center:
                startNode = home
            if end == home.rect.center:
                endNode = home
        
        if len(self.lines[-1]) == 2:
            startNode = self.originate
        
        if not self.check_collision(start, end, startNode, endNode):
            self.lines[-1].append(end)
            if endNode:
                endNode.connected[self.originate] = True
            return True
        else:
            return False

        


    def draw_lines(self, pos):
        self.collision_point = None
        self.err_message = None
        if not self.originate:
            for util in self.utilities:
                if util.rect.collidepoint(pos):
                    self.originate = util
                    self.lines.append([util, util.rect.center])
        
        else:
            terminates = False
            start = self.lines[-1][-1]
            nodes = []
            nodes.append(start)
            for home in self.homes:
                if home.rect.clipline(start[0], start[1], pos[0], pos[1]) and home.rect.center != start:
                    nodes.append(home.rect.center)
                if home.rect.collidepoint(pos):
                    terminates = True
            if not terminates:
                nodes.append(pos)

            nodes = sorted(nodes, key=cmp_to_key(lambda x, y: self.dist(x, start) - self.dist(y, start)))
            
            prevNode = start
            i = 1
            collided = False
            while i < len(nodes):
                collided = collided or not self.draw_line(prevNode, nodes[i])
                prevNode = nodes[i]
                if collided:
                    break
                i = i + 1
            
            if terminates and not collided: # if the supply line is terminating but already collided, then originate should remain active instead of getting set to None
                self.originate = None

    def run(self):
        self.is_running = True

        while self.is_running:
            while Gtk.events_pending():
               Gtk.main_iteration()

            self.py_events = pygame.event.get()
            for event in self.py_events:
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.size[0], event.size[1]),pygame.RESIZABLE)
                    self.reset()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.draw_lines(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_s:
                        self.originate = None
            
            self.draw()
    
            pygame.display.update()
            self.clock.tick(30)


if __name__ == "__main__":
    g = ThreeUtilities()
    GAME_SIZE = (800, 600)
    g.screen = pygame.display.set_mode(GAME_SIZE, pygame.RESIZABLE)
    g.run()