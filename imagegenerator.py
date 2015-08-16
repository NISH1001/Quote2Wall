#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
import time
import re
import textwrap

from exception import ManualError

def text_wrap(string, w):
    return textwrap.wrap(string, width=w)

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

    def create_text(
            self, text="", 
            font_size=25, font_color=(255,255,255), font_coord=(0,0), 
            wrap=False, wrap_length=20,
            align="MIDDLE"):
        try:
            self.font = ImageFont.truetype(self.font_path, font_size)
            if not self.draw or not self.image:
                raise ManualError("lol, cannot draw")

            if not wrap:
                font_coord = self.__align(align, font_size, font_coord, len(text.split("\n")) )
                self.draw.text( font_coord, text, font_color, font=self.font)
                self.draw = ImageDraw.Draw(self.image)
                return self.image

            else:
                para = text_wrap(text, wrap_length)
                font_coord = self.__align(align, font_size, font_coord, len(para) )
                curx,cury = font_coord
                pad = 10
                for line in para:
                    w,h = self.draw.textsize(line, font=self.font)
                    self.draw.text( ((self.width-w)/2, cury), line, font=self.font)
                    cury += h+pad

                self.draw = ImageDraw.Draw(self.image)
                return self.image

        except ManualError as merr:
            merr.display()
            return False

    def __align(self, align, font_size, font_coord, n):
        if align == "TOP":
            return (font_coord[0], 0)
        if align == "BOTTOM":
            return (font_coord[0], self.height-font_size*n*2)
        if align == "MIDDLE":
            return (font_coord[0], self.height/2 - n*font_size/2)
        else:
            return font_coord

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
    image = imggen.create_text(
            #text="Hello world!\nI am a moron\nand yes\ni can play something", 
            text="Hello world i am a moron and I am highly contagious",
            font_size=25, 
            font_color=(255,255,255), 
            font_coord=(350,0), 
            wrap=True, wrap_length=20,
            align="MIDDLE"
        )
    imggen.save_image(image, 'test')


if __name__=="__main__":
    main()

