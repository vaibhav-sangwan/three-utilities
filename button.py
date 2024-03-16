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


class Button(pygame.sprite.Sprite):
    def __init__(self, offcx, offcy, states, prompts):
        super().__init__()

        self.states = states
        self.prompts = prompts
        self.curr_state = 0
        self.active = False
        self.offcx = offcx
        self.offcy = offcy
        self.image = pygame.image.load(
            "./assets/" + self.states[self.curr_state] + ".png"
        )
        self.rect = self.image.get_rect(center=(0, 0))

    def reset_state(self):
        self.active = False
        self.curr_state = 0

    def update(self, py_events):
        for event in py_events:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = True
                else:
                    self.active = False

        image_dir = "./assets/" + self.states[self.curr_state]
        if self.active:
            image_dir += "-active"
        image_dir += ".png"
        self.image = pygame.image.load(image_dir)

    def toggle_state(self):
        self.curr_state += 1
        self.curr_state %= len(self.states)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def screen_resize(self, screen):
        self.rect.centery = screen.get_height() - 30
