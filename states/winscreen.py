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
from components.levelbutton import LevelButton
from gettext import gettext as _


class WinScreen:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        self.bound = pygame.image.load("./assets/images/bound.png")
        self.bound_rect = self.bound.get_rect(center=(
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        ))

        self.win_img = pygame.image.load("./assets/images/util-win.png")
        self.win_img_rect = self.win_img.get_rect(center=(
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        ))

        self.res_button = LevelButton(
            685, 570, ["restart"], [_("Restart Game")]
        )
        self.home_button = LevelButton(
            725,
            569,
            ['home-button'],
            [_("Main Menu")]
        )
        self.buttons = [self.res_button, self.home_button]

    def reset(self):
        pass

    def render(self):
        self.screen.fill("white")
        self.screen.blit(self.bound, self.bound_rect)
        for button in self.buttons:
            button.draw(self.screen)
        self.screen.blit(self.win_img, self.win_img_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.home_button.check_press():
                self.gameStateManager.set_state("main-menu")
            if self.res_button.check_press():
                self.gameStateManager.set_level(1, 1)
                self.game.states[self.gameStateManager.get_state()].reset()

    def run(self):
        for button in self.buttons:
            button.update()
        self.render()
