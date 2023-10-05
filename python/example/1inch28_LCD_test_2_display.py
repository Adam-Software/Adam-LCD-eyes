#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys 
import time
import logging
import RPi.GPIO as GPIO
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image, ImageDraw, ImageFont, ImageSequence

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
GPIO.setup(23, GPIO.OUT)           # set GPIO23 as an output
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output
GPIO.output(23, 0)         # set GPIO23 to 1/GPIO.HIGH/True
GPIO.output(24, 0)         # set GPIO24 to 1/GPIO.HIGH/True

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    # disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device), spi_freq=10000000, rst=RST, dc=DC, bl=BL)
    disp = LCD_1inch28.LCD_1inch28()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()


    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    gif_paths = [
    '../pic/Adam-Black-eyes-злится.gif',
    '../pic/Adam Black eyes моргает.gif',
    '../pic/Adam-Black-eyes-смотрит-влево-и-прямо.gif',
    '../pic/ROBOT ADAM EYES/Влюблен/Adam-Black-eyes-влюблен.gif',
    '../pic/ROBOT ADAM EYES/Восхищен/Adam-Black-eyes-восхищен.gif',
    '../pic/ROBOT ADAM EYES/Злится/Adam-Black-eyes-злится.gif',
    '../pic/ROBOT ADAM EYES/Плачет/Adam-Black-eyes-плачет.gif',
    '../pic/ROBOT ADAM EYES/Радуется/Adam-Black-eyes-радуется.gif',
    '../pic/ROBOT ADAM EYES/Смущен/RIGHT/Adam-Black-eyes-смущен-RIGHT.gif',
    '../pic/ROBOT ADAM EYES/Adam-Black-eyes-расширяются-зрачки.gif',
    '../pic/ROBOT ADAM EYES/Adam-Black-eyes-подмигивает-RIGHT.gif',
    '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смеется-RIGHT.gif',
    '../pic/ROBOT ADAM EYES/ANIME EYES/Adam-Anime-eyes-смотрит-по-сторонам.gif',
    '../pic/ROBOT ADAM EYES/CARTOON BLUE EYES/Adam-Cartoon-Blue-eyes-моргает.gif'
    # Add more GIF file paths as needed
    ]

    for gif_path in gif_paths:
        gif = Image.open(gif_path)

        # Получение списка кадров GIF
        frames = [gif.copy() for frame in ImageSequence.Iterator(gif)]
        num_frames = len(frames)

        # Вывод количества кадров
        print(f'Количество кадров в GIF: {num_frames}')

        for frame in frames:
            frame_rgb = frame.convert('RGB')
            disp.ShowImage(frame_rgb)
            time.sleep(0.15)

        # GPIO.output(24, 1)  # set GPIO24 to 1/GPIO.HIGH/True
        # disp.clear()

    disp.module_exit()
    logging.info("quit:")

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()




