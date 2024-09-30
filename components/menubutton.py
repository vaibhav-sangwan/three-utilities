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


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, active_path, inactive_path):
        super().__init__()

        self.inactive_img = pygame.image.load(inactive_path)
        self.active_img = pygame.image.load(active_path)
        self.image = self.inactive_img

        self.rect = self.image.get_rect(center=(x, y))

    def check_press(self):
        if self.rect.collidepoint(Utils.norm_cursor_pos()):
            return True
        return False

    def update(self):
        if self.rect.collidepoint(Utils.norm_cursor_pos()):
            self.image = self.active_img
        else:
            self.image = self.inactive_img
