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
from pygame import mixer
pygame.init()
from home import Home
from utility import Utility

INS_FONT = pygame.font.SysFont('ubuntumono', 18, bold=True)
ERROR_FONT = pygame.font.SysFont('ubuntumono', 24, bold=True)
INSTRUCTIONS = ["R - Restart", "S - Stop line", "M - Toggle Mute"]
ACHIEVEMENT_SOUND = mixer.Sound('assets/sounds/bonus.mp3')
WIN_SOUND = mixer.Sound('assets/sounds/win.mp3')
UTILITIES = [("water", "blue"), ("electricity", "red"), ("gas", "green")]

class ThreeUtilities:
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption('Three Utilities')
        self.clock = pygame.time.Clock()
        self.mute = False
        self.sound_channel = mixer.find_channel(True)
        self.level = [1, 1]
        self.load_level(self.level)
    
    def load_level(self, level):
        self.screen = pygame.display.get_surface()
        if not self.screen:
            self.screen = pygame.display.set_mode((800, 600))
        w, h = self.screen.get_width(), self.screen.get_height()

        self.utilities = []
        utils, houses = level
        mid = w/2
        dist = 200

        util_wid = (utils - 1) * dist
        util_start = mid - (util_wid/2)
        for i in range(1, utils + 1):
            self.utilities.append(Utility(util_start + ((i - 1) * dist), h/2 - 100, UTILITIES[i - 1][0], UTILITIES[i - 1][1]))

        self.homes = []
        house_wid = (houses - 1) * dist
        house_start = mid - (house_wid/2)
        for i in range(1, houses + 1):
            self.homes.append(Home(house_start + ((i - 1) * dist), h/2 + 100, self.utilities))
    
        self.originate = None
        self.lines = []

        self.err_message = None
        self.collision_point = None

        self.new_connects = 0
        self.total_connects = 0

        self.state = "running"
    
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

            circ_dist = 16
            circ_wid = (len(home.connected) - 1) * circ_dist
            circ_start = home.rect.centerx - (circ_wid/2)
            i = 0
            for util in home.connected:
                pygame.draw.circle(self.screen, util.color, (circ_start + (i * circ_dist), home.rect.bottom + 15), 5, 2 if not home.connected[util] else 0)
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
        
        if self.state == "running":
            level_msg = ERROR_FONT.render("LEVEL " + str(self.level[0] + self.level[1] - (1 if self.level[0] == 1 else 0)), False, "black")
            level_msg_rect = level_msg.get_rect(center = (self.screen.get_width()/2, 20))
            self.screen.blit(level_msg, level_msg_rect)

        if self.state == "win":
            win_msg = pygame.image.load("./assets/util-win.png")
            win_msg_rect = win_msg.get_rect(center = (self.screen.get_width()/2, self.screen.get_height()/2))
            self.screen.blit(win_msg, win_msg_rect)
        
        
    
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
                self.new_connects += 1
                endNode.connected[self.originate] = True
            return True
        else:
            return False

    def draw_lines(self, pos):
        self.new_connects = 0
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
                    self.load_level(self.level)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "running":
                    self.draw_lines(pygame.mouse.get_pos())
                    self.total_connects += self.new_connects
                    if self.total_connects >= self.level[0] * self.level[1]:
                        self.sound_channel.play(WIN_SOUND)
                        if self.level[0] == 3:
                            self.homes = []
                            self.utilities = []
                            self.lines = []
                            self.state = "win"
                        else:
                            self.level[1] += 1
                            if(self.level[1] > 3):
                                self.level[0] += 1
                                self.level[1] = self.level[0]
                            self.load_level(self.level)
                    elif self.new_connects > 0:
                        self.sound_channel.play(ACHIEVEMENT_SOUND)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.state == "win":
                            self.level = [1, 1]
                        self.load_level(self.level)
                    elif event.key == pygame.K_s:
                        self.originate = None
                    elif event.key == pygame.K_m:
                        self.mute = not self.mute
                        self.sound_channel.set_volume(0 if self.mute else 1)
            
            self.draw()
    
            pygame.display.update()
            self.clock.tick(30)


if __name__ == "__main__":
    g = ThreeUtilities()
    GAME_SIZE = (800, 600)
    g.screen = pygame.display.set_mode(GAME_SIZE, pygame.RESIZABLE)
    g.run()