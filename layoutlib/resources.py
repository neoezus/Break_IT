import os
import json
import pygame as pg


SOUND_TITLE = 0
SOUND_VOLUME = 1
FONT_NAME = 0
FONT_SIZE = 1


class Resources(object):

    def __init__(self, mainPath=''):
        # Initialize the Resources object with the mainPath
        self.mainPath = mainPath
        self.sound_ref = 0
        self.music_ref = 0
        self.font_ref = 0
        self.image_ref = 0
        self.persiLayer = ''
        self.screen = pg.display.get_surface()

    def load_sound(self, name, volume=1.0):
        # Load a sound file and set its volume
        name = os.path.join(self.mainPath, name)
        sound = pg.mixer.Sound(name)
        sound.set_volume(volume)
        assert sound
        self.sound_ref += 1
        return sound

    def load_snd_list(self, soundList):
        # Load a list of sound files
        sounds = []
        for snd in soundList:
            sounds.append(self.load_sound(snd[SOUND_TITLE], snd[SOUND_VOLUME]))
        return sounds

    def load_image(self, name, flag=None):
        # Load an image file
        if flag == 'alpha':
            image = pg.image.load(os.path.join(self.mainPath, name)).convert_alpha()
        else:
            image = pg.image.load(os.path.join(self.mainPath, name)).convert()
        assert image
        self.image_ref += 1
        return image

    def get_music_list(self, musicList):
        # Return a list of music file paths
        music_path = []
        for title in musicList:
            music_path.append(os.path.join(self.mainPath, title))
            self.music_ref += 1
        return music_path

    def load_img_list(self, imgList, flag=None):
        # Load a list of image files
        image = []
        for name in imgList:
            image.append(self.load_image(name, flag))
        return image

    def load_font(self, name, size):
        # Load a font file
        name = os.path.join(self.mainPath, name)
        font = pg.font.Font(name, size)
        assert font
        self.font_ref += 1
        return font

    def load_fnt_list(self, fntList):
        # Load a list of font files
        fonts = []
        for fnt in fntList:
            fonts.append(self.load_font(fnt[FONT_NAME], fnt[FONT_SIZE]))
        return fonts

    def print_font(self, font, message, vect, color=(255, 255, 255)):
        # Print text on the screen using a font
        self.screen.blit(font.render(message, True, color), vect)

    def load_global(self, imgList, sndList, fntList, mscList):
        # Load resources globally
        img = self.load_img_list(imgList)
        snd = self.load_snd_list(sndList)
        fnt = self.load_fnt_list(fntList)
        msc = self.get_music_list(mscList)
        return img, snd, fnt, msc

    def destroy_global(self):
        # Destroy global resources
        pass

    def save_res_info(self, data, fileName, indent=True):
        # Save resource information to a JSON file
        if not indent:
            inf = json.dumps(data)
        else:
            inf = json.dumps(data, indent=4, sort_keys=True)
        fileName = os.path.join(self.mainPath, fileName)
        with open(fileName, "w") as fp:
            fp.write(inf)
        fp.close()

    def get_res_info(self, fileName):
        # Get resource information from a JSON file
        self.persiLayer = fileName
        fileName = os.path.join(self.mainPath, fileName)
        with open(fileName, "r") as fp:
            str = fp.read()
        fp.close()

        return json.loads(str)

