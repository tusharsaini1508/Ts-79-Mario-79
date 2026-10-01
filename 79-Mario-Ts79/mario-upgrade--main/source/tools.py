"""
MIT License

Copyright (c) 2025 Tushar Saini 79 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


__author__ = 'Tushar Saini 79'

import os
import pygame as pg
from abc import ABC, abstractmethod

# Dictionary defining keybindings for different actions
keybinding = {
    'action': pg.K_s,
    'jump': pg.K_SPACE,
    'left': pg.K_LEFT,
    'right': pg.K_RIGHT,
    'down': pg.K_DOWN
}

# Class representing a State
class State():
    def __init__(self):
        # State variables
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.next = None
        self.persist = {}

    @abstractmethod
    def startup(self, current_time, persist):
        '''Abstract method to be overridden in child classes'''

    def cleanup(self):
        # Reset the state after it's done
        self.done = False
        return self.persist

    @abstractmethod
    def update(self, surface, keys, current_time):
        '''Abstract method to be overridden in child classes'''

# Class representing the Control for game states
class Control():
    def __init__(self):
        # Control variables
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.paused = False
        self.pause_started_at = 0
        self.pause_game_time = 0
        self.paused_duration = 0
        self.paused_surface = None
        self.pause_font = pg.font.Font(None, 32)
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        # Set up game states
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        # Update current game state
        if self.paused:
            self.current_time = self.pause_game_time
            self.draw_pause_overlay()
            return

        self.current_time = pg.time.get_ticks() - self.paused_duration
        if self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def toggle_pause(self):
        if self.paused:
            self.paused_duration += pg.time.get_ticks() - self.pause_started_at
            self.paused = False
        else:
            self.paused = True
            self.pause_started_at = pg.time.get_ticks()
            self.pause_game_time = self.current_time
            self.paused_surface = self.screen.copy()

    def draw_pause_overlay(self):
        if self.paused_surface is None:
            return

        self.screen.blit(self.paused_surface, (0, 0))
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        label = self.pause_font.render('PAUSED - PRESS P TO RESUME', True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=self.screen.get_rect().center))

    def flip_state(self):
        # Switch to the next game state
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def event_loop(self):
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.toggle_pause()
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def main(self):
        # Main game loop
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)

# Function to get an image from a sprite sheet
def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pg.Surface([width, height])
    rect = image.get_rect()

    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pg.transform.scale(image, (int(rect.width*scale), int(rect.height*scale)))
    return image

# Function to load all graphics from a specified directory
def load_all_gfx(directory, colorkey=(255, 0, 255), accept=('.png', '.jpg', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics
