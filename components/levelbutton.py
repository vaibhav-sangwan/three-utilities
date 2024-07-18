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
PROMPT_FONT = pygame.font.SysFont("ubuntumono", 18, bold=True)


class LevelButton(pygame.sprite.Sprite):
    def __init__(self, x, y, states, prompts):
        super().__init__()

        self.states = states
        self.prompts = prompts

        self.images = []
        for state in self.states:
            image_pair = []
            image_pair.append(pygame.image.load("./assets/images/" + state + ".png"))
            image_pair.append(pygame.image.load("./assets/images/" + state + "-active.png"))
            self.images.append(image_pair)
        self.state = [0, 0]
        self.image = self.images[self.state[0]][self.state[1]]
        self.rect = self.image.get_rect(center=(x, y))
    
    def reset(self):
        self.state = [0, 0]

    def update(self):
        if self.rect.collidepoint(Utils.norm_cursor_pos()):
            self.state[1] = 1
        else:
            self.state[1] = 0

        self.image = self.images[self.state[0]][self.state[1]]

    def check_press(self):
        if self.rect.collidepoint(Utils.norm_cursor_pos()):
            self.toggle_state()
            return True
        return False

    def toggle_state(self):
        self.state[0] += 1
        self.state[0] %= len(self.states)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.state[1] == 1:
            prompt_text = PROMPT_FONT.render(
                self.prompts[self.state[0]], False, "black"
            )
            prompt_rect = prompt_text.get_rect(
                center=(self.rect.centerx, self.rect.top - 10)
            )
            screen.blit(prompt_text, prompt_rect)
