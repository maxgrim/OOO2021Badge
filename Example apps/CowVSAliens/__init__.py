#!/usr/bin/env python3

# Created by: Mr. Coxall
# Created on: Sep 2019
# This file is the "Space Aliens" game
#   for CircuitPython

import stage
import board
import time
import random
import constants
import supervisor
from io_expander import IOExpander

io_expander = IOExpander(board.I2C())

def splash_scene():
    # this function is the splash scene game loop

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, 160, 120)
    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(board.DISPLAY, 60)
    # set the layers, items show up in order
    game.layers = [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block(0, 0, 320, 240)

    # repeat forever, game loop
    while True:
        # get user input

        # Wait for 1 seconds
        time.sleep(1.0)
        menu_scene()

        # redraw sprite list

def menu_scene():
    # this function is the menu scene

    # an image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    # used this program to split the iamge into tile: https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    text = []
    
    text1 = stage.Text(width=29, height=14, font=None, palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text1.move(120, 80)
    text1.text("COWS vs ALIENS")
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None, palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text2.move(120, 120)
    text2.text("PRESS START")
    text.append(text2)

    # get sound ready
    # follow this guide to convert your other sounds to something that will work
    #    https://learn.adafruit.com/microcontroller-compatible-audio-file-conversion
    

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(board.DISPLAY, 60)
    # set the layers, items show up in order
    game.layers = text + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()
    # repeat forever, game loop
    while True:
        # get user input
        io_expander.update()
        if io_expander.button_start.fell:
            game_scene()
            break  

def game_scene():
    # this function is the game scene
    print("Game entered")
    # game score
    score = 0

    def show_alien():
        # I know this is a function that is using variables outside of itself!
        #   BUT this code is going to be used in 2 places :)
        # make an alien show up on screen in the x-axis
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0: # meaning it is off the screen, so available to move on the screen
                aliens[alien_number].move(random.randint(0 + constants.SPRITE_SIZE, constants.SCREEN_X - constants.SPRITE_SIZE), constants.OFF_TOP_SCREEN)
                break

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")
    # a list of sprites that will be updated every frame
    sprites = []

    # create lasers for when we shoot
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_1, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_X)
        lasers.append(a_single_laser)

    # create aliens
    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_1, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_X)
        aliens.append(a_single_alien)

    # current number of aliens that should be moving down screen, start with just 1
    alien_count  = 1
    show_alien()

    # add text at top of screen for score
    score_text = stage.Text(width=29, height=14, font=None, palette=constants.SCORE_PALETTE, buffer=None)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(1, 1)
    score_text.text("Score: {0}".format(score))

    ship = stage.Sprite(image_bank_1, 5, int(constants.SCREEN_X / 2), constants.SCREEN_Y - constants.SPRITE_SIZE)
    sprites.append(ship) # insert at the top of sprite list

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)


    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(board.DISPLAY, 60)
    # set the layers, items show up in order
    game.layers = sprites + lasers + aliens + [score_text] + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        io_expander.update()

        if io_expander.button_right.value:
        #if ship moves off right screen, move it back
             if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                 ship.x = constants.SCREEN_X - constants.SPRITE_SIZE
        # else move ship right
             else:
                 ship.move(ship.x + constants.SHIP_SPEED, ship.y)    
        
        if io_expander.button_left.value:
        # if ship moves off left screen, move it back
            if ship.x < 0:
                ship.x = 0
        #     # else move ship left
            else:
                ship.move(ship.x - constants.SHIP_SPEED, ship.y)
        if io_expander.button_center.fell or io_expander.button_a.fell:
        # fire a laser, if we have enough power (meaning we have not used up all the lasers)
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    break
        # each frame move the lasers, that have been fired, up
        lasers_moving_counter = -1
        
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x, lasers[laser_number].y - constants.LASER_SPEED)
                lasers_moving_counter = lasers_moving_counter + 1
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # each frame move the aliens down the screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0: # meaning it is on the screen
                aliens[alien_number].move(aliens[alien_number].x, aliens[alien_number].y + constants.ALIEN_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien() # make it randomly show up at top again

        # each frame check if any of the lasers are touching any of the aliens
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0 :
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:
                        # https://circuitpython-stage.readthedocs.io/en/latest/#stage.collide
                        # and https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other

                        # the first 4 numbers are the coordinates of A box
                        # since the laser is thin, it made it thinner and slightly smaller
                        #
                        # the second 4 numbers are the alien, it is more of a box so I just made it slightly smaller
                        #
                        # if you slow down the FPS, then you can see the interaction more easily to alter these numbers
                        if stage.collide(lasers[laser_number].x + 6, lasers[laser_number].y + 2,
                                         lasers[laser_number].x + 11, lasers[laser_number].y + 12,
                                         aliens[alien_number].x + 1, aliens[alien_number].y,
                                         aliens[alien_number].x + 15, aliens[alien_number].y + 15):
                            # you hit an alien
                            aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            # add 1 to the score
                            score += 1
                            score_text.clear()
                            score_text.cursor(0, 0)
                            score_text.move(1, 1)
                            score_text.text("Score: {0}".format(score))
                            # this will freeze the screen for a split second, but we have no option
                            game.render_block()
                            show_alien()
                            alien_count = alien_count + 1

        # each frame check if any of the aliens are touching the ship
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                # https://circuitpython-stage.readthedocs.io/en/latest/#stage.collide
                # and https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other
                if stage.collide(aliens[alien_number].x + 1, aliens[alien_number].y,
                                 aliens[alien_number].x + 15, aliens[alien_number].y + 15,
                                 ship.x, ship.y,
                                 ship.x + 15, ship.y + 15):
                    # alien hit the ship
                    # Wait for 1 seconds
                    time.sleep(1.0)
                    game_over_scene(score)

        # redraw sprite list
        game.render_sprites(sprites + lasers + aliens)
        game.tick() # wait until refresh rate finishes

def game_over_scene(final_score):
    # this function is the game over scene
    # an image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")
    print (final_score)
    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    text = []

    text0 = stage.Text(width=29, height=14, font=None, palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text0.move(120, 100)
    text0.text("Final Score: {:0>2d}".format(final_score))
    text.append(text0)

    text1 = stage.Text(width=29, height=14, font=None, palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text1.move(120, 80)
    text1.text("GAME OVER")
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None, palette=constants.MT_GAME_STUDIO_PALETTE, buffer=None)
    text2.move(120, 120)
    text2.text("PRESS START")
    text.append(text2)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(board.DISPLAY, 60)
    # set the layers, items show up in order
    game.layers = text + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    while True:
        io_expander.update()

        if io_expander.button_start.fell:
            menu_scene()
        if io_expander.button_menu.fell:
            return

def main():
    splash_scene()

