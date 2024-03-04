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

class Utility(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color):
        super().__init__()
        self.type = type
        self.color = color
        self.image = pygame.image.load('./assets/' + self.type + '.png')
        self.rect = self.image.get_rect(center = (x, y))
        self.active = False
    
    def update(self, py_events):
        for event in py_events:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = True
                    self.image = pygame.image.load('./assets/' + self.type + '-active.png')
                else:
                    self.active = False
                    self.image = pygame.image.load('./assets/' + self.type + '.png')