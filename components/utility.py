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

from utils import Utils


class Utility(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color):
        super().__init__()
        self.type = type
        self.color = color
        self.inactive_img = pygame.image.load('./assets/images/' + self.type + '.png')
        self.active_img = pygame.image.load('./assets/images/' + self.type + '-active.png')
        self.image = self.inactive_img
        self.rect = self.image.get_rect(center=(x, y))
        self.active = False

    def update(self):
        if self.rect.collidepoint(Utils.norm_cursor_pos()):
            self.image = self.active_img
            self.active = True
        else:
            self.image = self.inactive_img
            self.active = False
