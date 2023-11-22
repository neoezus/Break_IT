import pygame as pg
import sys



class Window(object):
    """ Window : Contain the whole game,window, resources...etc """

    def __init__(self,
                 screenWidth,
                 screenHeight,
                 fullscreen,
                 windowTitle):

        # full screen & optimization
        flag = 1
        # init pygame
        pg.init()
        if not pg.display.get_init():
            print('unable to init display pygame')
            self.destroy()
        else:
            pg.display.set_caption(windowTitle)
            if fullscreen:
                flag |= pg.FULLSCREEN
            flag |= pg.HWSURFACE
            flag |= pg.DOUBLEBUF
            pg.display.set_mode((screenWidth, screenHeight), flag)
            # temporarily set which modifier keys are pressed to 0.
            pg.key.set_mods(0)
            pg.key.set_repeat(10, 10)

    def load_complete(
            self,
            instance,
            dataFolder,
            persistenceLayer,
            fileLevels):

        # display infos
        print('Display driver: ' + pg.display.get_driver())
        print(pg.display.Info())
        # get instance of the game:
        self.gInstance = instance
        # load game resources & get infos from persistence layer.
        self.gInstance.load_game(dataFolder, persistenceLayer)
        self.gInstance.load_levels(dataFolder, fileLevels)

    def destroy(self):
        if self.gInstance:
            self.gInstance.destroy_game()
        pg.quit()
