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

def numofframe(gifpath):

    gif = Image.open(gifpath)

    # Получение списка кадров GIF
    frames = [gif.copy() for frame in ImageSequence.Iterator(gif)]
    num_frames = len(frames)

    # Вывод количества кадров
    print(f'Количество кадров в GIF: {num_frames}')
    return frames

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

    gif_paths_R = [
        '../pic/ROBOT ADAM EYES/Adam Black eyes СТАТИЧНЫЙ ГЛАЗ.png',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смеется-RIGHT.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-расширяются-зрачки.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смущен-RIGHT.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-подмигивает-RIGHT.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-расширяются-зрачки.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смотрит-по-сторонам.gif',
        '../pic/ROBOT ADAM EYES/Adam Black eyes СТАТИЧНЫЙ ГЛАЗ.png',
    # Add more GIF file paths as needed
    ]

    gif_paths_L = [
        '../pic/ROBOT ADAM EYES/Adam Black eyes СТАТИЧНЫЙ ГЛАЗ.png',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смеется-LEFT.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-подмигивает-LEFT.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смущен-LEFT.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-расширяются-зрачки.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-расширяются-зрачки.gif',
        '../pic/ROBOT ADAM EYES/Adam-Black-eyes-смотрит-по-сторонам.gif',
        '../pic/ROBOT ADAM EYES/Adam Black eyes СТАТИЧНЫЙ ГЛАЗ.png',
       # Add more GIF file paths as needed
    ]

    for gif_path_R, gif_path_L in zip(gif_paths_R, gif_paths_L):
        frames_R = numofframe(gif_path_R)
        frames_L = numofframe(gif_path_L)
        time.sleep(2.0)

        for frame_L, frame_R in zip(frames_L, frames_R):
            GPIO.output(23, 1)  # set GPIO24 to 1/GPIO.HIGH/True
            GPIO.output(24, 0)  # set GPIO24 to 1/GPIO.HIGH/True
            frame_rgb_L = frame_L.convert('RGB')
            disp.ShowImage(frame_rgb_L)

            frame_rgb_R = frame_R.convert('RGB')
            GPIO.output(23, 0)  # set GPIO24 to 1/GPIO.HIGH/True
            GPIO.output(24, 1)  # set GPIO24 to 1/GPIO.HIGH/True
            disp.ShowImage(frame_rgb_R)
            time.sleep(0.05)

    time.sleep(3.0)

    GPIO.output(23, 0)  # set GPIO24 to 1/GPIO.HIGH/True
    GPIO.output(24, 0)  # set GPIO24 to 1/GPIO.HIGH/True

    disp.clear()

    disp.module_exit()
    logging.info("quit:")

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
