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

import pygame
pygame.init()

class ThreeUtilities:
    def __init__(self):
        pygame.display.init()
        pygame.display.set_caption('Three Utilities')
        self.clock = pygame.time.Clock()

    def run(self):
        self.screen = pygame.display.get_surface()
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
            
            pygame.display.update()
            self.clock.tick(30)


if __name__ == "__main__":
    g = ThreeUtilities()
    GAME_SIZE = (800, 600)
    g.screen = pygame.display.set_mode(GAME_SIZE, pygame.RESIZABLE)
    g.run()