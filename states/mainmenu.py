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

import pygame
import math
import random

from components.menubutton import MenuButton

LINE_SPEED = 10
LINE_LENGTH = 40
GRID_HOR_SPACE = 80
GRID_VER_SPACE = 60
GRID_COLOR = (0, 0, 0, 64)

class MainMenu:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        self.grid = []
        for i in range(11):
            curr = [False for j in range(11)]
            self.grid.append(curr)
        
        self.lines = []
        self.bg = pygame.image.load("./assets/images/main-menu-bg.png")
        self.bg_rect = self.bg.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))

        self.logo = pygame.image.load("./assets/images/logo.png")
        self.logo_rect = self.logo.get_rect(center=(400, 120))

        self.play_button = MenuButton(400, 290, "./assets/images/play-button-active.png", "./assets/images/play-button.png")
        self.help_button = MenuButton(400, 410, "./assets/images/help-button-active.png", "./assets/images/help-button.png")
        
    def emit_line(self):
        si = random.randint(1, 9)
        sj = random.randint(1, 9)
        
        # 0 is added twice to make the probabilty of
        # moving in vertical direction equal to that of
        # moving in horizontal direction
        dx = random.choice([-1, 0, 0, 1])
        if dx == 0:
            dy = random.choice([-1, 1])
        else:
            dy = 0
        
        ei = si + dx
        ej = sj + dy
        color = random.choice(["red", "green", "blue"])
        speed = 10
        if (not self.grid[si][sj]) or (not self.grid[ei][ej]):
            self.grid[si][sj] = True
            self.grid[ei][ej] = True
            sx = si * GRID_HOR_SPACE
            sy = sj * GRID_VER_SPACE
            ex = ei * GRID_HOR_SPACE
            ey = ej * GRID_VER_SPACE
            self.lines.append(
                {
                    "sindex": (si, sj),
                    "eindex": (ei, ej),
                    "start": [sx, sy],
                    "end": [ex, ey],
                    "color": color,
                    "orig": [sx, sy],
                    "term": [sx, sy],
                    "dx": dx * speed,
                    "dy": dy * speed,
                }
            )
        else:
            self.emit_line()
    
    def dist(self, start, end):
        return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    
    def update_lines(self):
        i = 0
        while i < (len(self.lines)):
            line = self.lines[i]
            if line["orig"] == line["end"]:
                self.lines.pop(i)
                self.grid[line["sindex"][0]][line["sindex"][1]] = False
                self.grid[line["eindex"][0]][line["eindex"][1]] = False
                
            
            if self.dist(line["orig"], line["term"]) < LINE_LENGTH and line["orig"] == line["start"]:
                line["term"][0] += line["dx"]
                line["term"][1] += line["dy"]
            elif line["term"] == line["end"]:
                line["orig"][0] += line["dx"]
                line["orig"][1] += line["dy"]
            else:
                line["orig"][0] += line["dx"]
                line["orig"][1] += line["dy"]
                line["term"][0] += line["dx"]
                line["term"][1] += line["dy"]
            
            i += 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.check_press():
                self.gameStateManager.set_level(1, 1)
                self.game.states[self.gameStateManager.get_state()].reset()
            if self.help_button.check_press():
                self.gameStateManager.set_state("help-menu")

    def render(self):
        self.screen.fill("white")
        for i in range(11):
            pygame.draw.line(self.screen, GRID_COLOR, (i * GRID_HOR_SPACE, 0), (i * GRID_HOR_SPACE, 600))
            pygame.draw.line(self.screen, GRID_COLOR, (0, i * GRID_VER_SPACE), (800, i * GRID_VER_SPACE))

        for i in range(1, 10):
            for j in range(1, 10):
                pygame.draw.circle(self.screen, GRID_COLOR, (i * GRID_HOR_SPACE, j * GRID_VER_SPACE), 3)
        for line in self.lines:
            pygame.draw.line(self.screen, line["color"], line["orig"], line["term"], 1)
            if line["term"] == line["end"]:
                pygame.draw.circle(self.screen, line["color"], line["end"], 3)
        
        self.screen.blit(self.bg, self.bg_rect)
        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.play_button.image, self.play_button.rect)
        self.screen.blit(self.help_button.image, self.help_button.rect)

    def run(self):
        while len(self.lines) < 50:
            self.emit_line()
        self.update_lines()
        self.play_button.update()
        self.help_button.update()
        self.render()
