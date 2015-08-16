#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
import time
import re

from exception import ManualError

class ImageGenerator:
    
    def __init__(self, width, height, font_path="/usr/share/fonts/dejavu/DejaVuSans.ttf"):
        self.width, self.height = width, height
        self.image = None
        self.draw = None
        self.font = None
        self.font_path = font_path

    def create_background(self, rgba):
        self.image = Image.new("RGBA", tuple([self.width, self.height]), rgba)
        self.draw = ImageDraw.Draw(self.image)
        return self.image

    def create_text(self, text="i am a moron", font_size=25, font_color=(255,255,255), font_coord=(0,0)):
        try:
            if not self.draw or not self.image:
                raise ManualError("lol, cannot draw")
            else:
                self.font = ImageFont.truetype(self.font_path, font_size)
                self.draw.text( font_coord, text, font_color, font=self.font)
                self.draw = ImageDraw.Draw(self.image)
                return self.image

        except ManualError as merr:
            merr.display()
            return False

    def save_image(self, image,  filename):
        if not filename:
            filename = re.sub(r'\.', '', str(time.time()))

        try:
            if not image:
                raise ManualError("create an image first :D")
            else:
                self.image.save(filename+'.png')
                return True

        except ManualError as merr:
            merr.display()
            return False

def main():
    imggen = ImageGenerator(800, 600)
    image = imggen.create_background( (0,0,0) )
    image = imggen.create_text(text="I am a \nmoron", font_size=25, font_color=(255,255,255), font_coord=(500,0))
    imggen.save_image(image, 'test')


if __name__=="__main__":
    main()

