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

import math
from functools import cmp_to_key
from utils import dist, segment_intersect, Utils

import pygame
from pygame import mixer

from components.home import Home
from components.utility import Utility
from components.levelbutton import LevelButton

from gettext import gettext as _

import pickle
import numpy

pygame.init()
font_s = pygame.font.Font("./fonts/m04b.ttf", 8)
font_m = pygame.font.Font("./fonts/m04b.ttf", 12)
font_l = pygame.font.Font("./fonts/3Dventure.ttf", 32)
ACHIEVEMENT_SOUND = mixer.Sound("assets/sounds/bonus.mp3")
WIN_SOUND = mixer.Sound("assets/sounds/win.mp3")
UTILITIES = [("water", "blue"), ("electricity", "red"), ("gas", "green")]
HINTS = [
    _("Uh-oh, the household needs some water."),
    _("The plumber has been called for laying water pipelines for two \
houses."),
    _("You've become the water supply engineer of your town, \
make sure that all the houses are connected."),
    _("Here comes a zap! You might need to bend some wires."),
    _("Water flows underground and Electricity is supplied through roofs."),
    _("Did you know that you can connect more than 1 household \
with a single supply line?"),
]


class Level:
    def __init__(self, game, num_utils, num_houses):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        self.bg = pygame.image.load("./assets/images/bound.png")
        self.bg_rect = self.bg.get_rect(center=(
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        ))

        self.level = [num_utils, num_houses]
        self.res_button = LevelButton(560, 570, ["restart"], [_("Restart")])
        self.mute_button = LevelButton(
            605,
            570,
            ["unmute", "mute"],
            [_("Mute"), _("Unmute")]
        )
        self.hint_button = LevelButton(
            645,
            570,
            ["show-hint", "hide-hint"],
            [_("Show Hint"), _("Hide Hint")]
        )
        self.sol_button = LevelButton(
            685,
            570,
            ["show-sol", "hide-sol"],
            [_("Show Solution"), _("Hide Solution")]
        )
        self.home_button = LevelButton(
            725,
            569,
            ['home-button'],
            [_("Main Menu")]
        )
        self.buttons = [
            self.home_button,
            self.res_button,
            self.mute_button,
            self.hint_button,
            self.sol_button,
        ]

        self.reset()

    def save_data(self, file):
        info = []
        print(self.lines)
        for line in self.lines:
            curr_info = [line[0].color]
            for j in range(1, len(line)):
                curr_info.append(
                    (
                        line[j][0] - self.screen.get_width() / 2,
                        line[j][1] - self.screen.get_height() / 2,
                    )
                )
            info.append(curr_info)
        with open(file, "wb") as fp:
            pickle.dump(info, fp)

    def reset(self):
        self.utilities = []
        utils, houses = self.level
        mid = 400
        dist = 200

        self.sol_button.reset()
        self.hint_button.reset()
        if self.game.mute:
            self.mute_button.state[0] = 1

        util_wid = (utils - 1) * dist
        util_start = mid - (util_wid / 2)
        for i in range(1, utils + 1):
            self.utilities.append(
                Utility(
                    util_start + ((i - 1) * dist),
                    160,
                    UTILITIES[i - 1][0],
                    UTILITIES[i - 1][1],
                )
            )

        self.homes = []
        house_wid = (houses - 1) * dist
        house_start = mid - (house_wid / 2)
        for i in range(1, houses + 1):
            self.homes.append(
                Home(
                    house_start + ((i - 1) * dist),
                    360,
                    self.utilities
                )
            )

        self.originate = None
        self.lines = []

        self.err_message = None
        self.collision_point = None

        self.new_connects = 0
        self.total_connects = 0

        self.show_solution = False
        self.show_hint = False

    def get_curr_level(self):
        res = self.level[0] + self.level[1]
        if self.level[0] == 1:
            res -= 1
        return res

    def draw_dashed_line(
        self, surf, color, start_pos, end_pos, width=1, dash_length=10
    ):
        x1, y1 = int(start_pos[0]), int(start_pos[1])
        x2, y2 = int(end_pos[0]), int(end_pos[1])
        dl = dash_length

        if x1 == x2:
            ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
            xcoords = [x1] * len(ycoords)
        elif y1 == y2:
            xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
            ycoords = [y1] * len(xcoords)
        else:
            a = abs(x2 - x1)
            b = abs(y2 - y1)
            c = round(math.sqrt(a**2 + b**2))
            dx = dl * a / c
            dy = dl * b / c

            xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
            ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

        next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
        last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
        for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
            start = (round(x1), round(y1))
            end = (round(x2), round(y2))
            pygame.draw.line(surf, color, start, end, width)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = Utils.norm_cursor_pos()
            if self.res_button.check_press():
                self.reset()
            elif self.mute_button.check_press():
                self.game.toggle_mute()
            elif self.sol_button.check_press():
                self.show_solution = not self.show_solution
            elif self.hint_button.check_press():
                self.show_hint = not self.show_hint
            elif self.home_button.check_press():
                self.gameStateManager.set_state("main-menu")
            else:
                self.draw_lines(mouse_pos)
                self.total_connects += self.new_connects
                if self.total_connects >= self.level[0] * self.level[1]:
                    self.game.sound_channel.play(WIN_SOUND)
                    if self.level[0] == 3:
                        self.gameStateManager.set_state("win-screen")
                    else:
                        houses = self.level[1] + 1
                        utils = self.level[0]
                        if houses > 3:
                            utils += 1
                            houses = utils
                        self.gameStateManager.set_level(utils, houses)
                        curr_state = self.gameStateManager.get_state()
                        self.game.states[curr_state].reset()
                elif self.new_connects > 0:
                    self.game.sound_channel.play(ACHIEVEMENT_SOUND)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.originate = None

    def render(self):
        self.screen.fill("white")
        self.screen.blit(self.bg, self.bg_rect)
        for button in self.buttons:
            button.draw(self.screen)

        if self.show_solution:
            with open("./solutions/" + str(self.get_curr_level()), "rb") as fp:
                help_lines = pickle.load(fp)

            scx = self.screen.get_width() / 2
            scy = self.screen.get_height() / 2
            for line in help_lines:
                for j in range(1, len(line) - 1):
                    start = (line[j][0] + scx, line[j][1] + scy - 40)
                    end = (line[j + 1][0] + scx, line[j + 1][1] + scy - 40)
                    self.draw_dashed_line(self.screen, line[0], start, end, 1)

        for i in range(len(self.lines)):
            line = self.lines[i]
            for j in range(1, len(line) - 1):
                pygame.draw.line(self.screen,
                                 line[0].color,
                                 line[j],
                                 line[j + 1],
                                 3)
            if (i == len(self.lines) - 1) and self.originate:
                pygame.draw.line(
                    self.screen,
                    line[0].color,
                    line[-1],
                    Utils.norm_cursor_pos(),
                    3
                )

        for home in self.homes:
            home.update()
            self.screen.blit(home.image,
                             (home.rect.left - 9, home.rect.top - 16))

            circ_dist = 16
            circ_wid = (len(home.connected) - 1) * circ_dist
            circ_start = home.rect.centerx - (circ_wid / 2)
            i = 0
            for util in home.connected:
                pygame.draw.circle(
                    self.screen,
                    util.color,
                    (circ_start + (i * circ_dist), home.rect.bottom + 15),
                    5,
                    2 if not home.connected[util] else 0,
                )
                i += 1

        for util in self.utilities:
            util.update()
            self.screen.blit(util.image, util.rect)

        if self.collision_point:
            pygame.draw.circle(self.screen, "red", self.collision_point, 5)
            error = font_m.render(self.err_message, False, "red")
            error_rect = error.get_rect(
                center=(self.screen.get_width() / 2,
                        self.screen.get_height() - 30)
            )
            self.screen.blit(error, error_rect)

        if self.show_hint:
            Utils.render_multiple_lines(
                HINTS[self.get_curr_level() - 1],
                self.screen,
                10,
                (10, 50),
                "black",
                font_s
            )

        disp_level = self.get_curr_level()
        level_msg = font_l.render(
            _("LEVEL ") + str(disp_level),
            False,
            "black",
        )
        level_msg_rect = level_msg.get_rect(
            center=(self.screen.get_width() / 2, 20)
        )
        self.screen.blit(level_msg, level_msg_rect)

    def lines_collide(self, ts, te, os, oe, originating, terminating):
        intersect_point = segment_intersect((ts, te), (os, oe))
        # when the line is connecting a supply to already connected house
        if terminating and terminating.connected[self.originate]:
            self.err_message = _("Already Connected")
            self.collision_point = terminating.rect.center
            return True
        # when the lines are coincident
        if (ts, te) == (os, oe) or (ts, te) == (oe, os):
            self.err_message = _("Collision")
            self.collision_point = te
            return True
        if not intersect_point:
            return False
        if intersect_point == ts and originating:
            return False
        if intersect_point == te and terminating:
            return False
        self.collision_point = intersect_point
        self.err_message = _("Collision")
        return True

    def check_collision(self, start, end, startNode, endNode):
        for i in range(len(self.lines)):
            line = self.lines[i]
            for j in range(1, len(line) - 1):
                if i == len(self.lines) - 1 and j == len(line) - 2:
                    continue
                if self.lines_collide(
                    start, end, line[j], line[j + 1], startNode, endNode
                ):
                    return True
        return False

    def draw_line(self, start, end):
        startNode = None
        endNode = None

        for home in self.homes:
            if start == home.rect.center:
                startNode = home
            if end == home.rect.center:
                endNode = home

        if len(self.lines[-1]) == 2:
            startNode = self.originate

        if not self.check_collision(start, end, startNode, endNode):
            self.lines[-1].append(end)
            if endNode:
                self.new_connects += 1
                endNode.connected[self.originate] = True
            return True
        else:
            return False

    def draw_lines(self, pos):
        self.new_connects = 0
        self.collision_point = None
        self.err_message = None
        if not self.originate:
            for util in self.utilities:
                if util.rect.collidepoint(pos):
                    self.originate = util
                    self.lines.append([util, util.rect.center])

        else:
            terminates = False
            start = self.lines[-1][-1]
            nodes = []
            nodes.append(start)
            for home in self.homes:
                passing = home.rect.clipline(start[0],
                                             start[1],
                                             pos[0],
                                             pos[1])
                if passing and home.rect.center != start:
                    nodes.append(home.rect.center)
                if home.rect.collidepoint(pos):
                    terminates = True
            if not terminates:
                nodes.append(pos)

            nodes = sorted(
                nodes,
                key=cmp_to_key(lambda x, y:
                               dist(x, start) - dist(y, start)),
            )

            prevNode = start
            i = 1
            collided = False
            while i < len(nodes):
                collided = collided or not self.draw_line(prevNode, nodes[i])
                prevNode = nodes[i]
                if collided:
                    break
                i = i + 1

            # if the supply line is terminating but
            # already collided, then originate should remain
            # active instead of getting set to None
            if terminates and not collided:
                self.originate = None

    def run(self):
        for button in self.buttons:
            button.update()
        self.render()
