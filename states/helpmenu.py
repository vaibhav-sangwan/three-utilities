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
from components.backbutton import BackButton

font_s = pygame.font.Font("./fonts/m04b.ttf", 16)
font_l = pygame.font.Font("./fonts/3Dventure.ttf", 64)
page_1 = """\
There are multiple levels in Three Utilities activity. All you need \
to do is to lay down supply lines from utilities to homes in such \
a manner that they dont cross each other. Also, every house must be \
connected with each utility available to progress to the next level.

Controls
You can use your mouse to lay supply lines. Click on a utility to \
initiate the line. Then the supply line would follow your cursor. \
Pressing Left Mouse Button would add a bend to the supply line. Press \
Left Mouse Button on any house to terminate the active supply line \
there. If there is an active supply line, and you want to terminate it \
without connecting it to a house, you can press S.
"""

pages = [page_1]


class HelpMenu:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game
        self.bg = pygame.image.load("./assets/images/bound.png")
        self.bg_rect = self.bg.get_rect(center=(
            self.screen.get_width()/2,
            self.screen.get_height()/2
        ))
        self.title = font_l.render("HELP", False, "black")
        self.title_rect = self.title.get_rect(center = (self.screen.get_width()/2, 40))
        self.backbtn = BackButton(750, 550)
        self.page = 0
        self.refresh_page()

    def reset(self):
        pass

    def refresh_page(self):
        self.curr_page = self.bg.copy()
        Utils.render_multiple_lines(
            pages[self.page], self.curr_page, 60, (60, 90), "black", font_s
        )
        self.curr_page_rect = self.curr_page.get_rect(center=(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        ))

    def render(self):
        self.screen.fill("white")
        self.screen.blit(self.bg, self.bg_rect)
        self.screen.blit(self.curr_page, self.curr_page_rect)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.backbtn.image, self.backbtn.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.backbtn.check_press():
                self.gameStateManager.set_state("main-menu")

    def run(self):
        self.backbtn.update()
        self.render()
