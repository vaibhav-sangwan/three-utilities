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

from gettext import gettext as _

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pygame
pygame.init()
from pygame import mixer

from utils import Utils
from gamestatemanager import GameStateManager
from states.level import Level

BASE_RES = (800, 600)
FPS = 30


class ThreeUtilities:
    def __init__(self):
        pygame.display.set_caption(_("Three Utilities"))
        self.clock = pygame.time.Clock()
        self.mute = False
        self.sound_channel = mixer.find_channel(True)

    def fill_bg(self):
        self.render_screen.fill("black")
    
    def toggle_mute(self):
        self.mute = not self.mute
        self.sound_channel.set_volume(0 if self.mute else 1)

    def run(self):
        self.screen = pygame.Surface(BASE_RES)
        self.render_screen = pygame.display.set_mode((0, 0))
        screen_width = self.render_screen.get_width()
        screen_height = self.render_screen.get_height()
        x_ratio = screen_width / BASE_RES[0]
        y_ratio = screen_height / BASE_RES[1]
        self.scale = min(x_ratio, y_ratio)
        act_sw = BASE_RES[0] * self.scale
        act_sh = BASE_RES[1] * self.scale
        self.scaled_screen_rect = pygame.Rect(0, 0, act_sw, act_sh)
        self.scaled_screen_rect.center = (screen_width / 2, screen_height / 2)
        Utils.scaled_screen_rect = self.scaled_screen_rect

        self.gameStateManager = GameStateManager("level-1-1")
        self.states = {}
        for i in range(1, 4):
            for j in range(i, 4):
                self.states["level-" + str(i) + "-" + str(j)] = Level(self, i, j)


        self.is_running = True
        while self.is_running:
            curr_state = self.states[self.gameStateManager.get_state()]

            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                curr_state.handle_event(event)

            curr_state.run()

            self.fill_bg()
            scaled_screen = pygame.transform.scale(
                self.screen,
                (self.scale * BASE_RES[0], self.scale * BASE_RES[1])
            )
            self.render_screen.blit(scaled_screen, self.scaled_screen_rect)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    g = ThreeUtilities()
    g.run()
