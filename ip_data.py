#!/usr/bin/python3

import os
import sys
import requests
import time
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Load e-ink screen lib
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

    from waveshare_epd import epd2in13bc

# picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
logging.basicConfig(level=logging.DEBUG)

# IP Data Logic
def ip_data():
    url = 'https://api-ipv4.ip.sb/geoip'

    # Required to prevent 403 responses
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error: {response.status_code} - {response.reason}")

try:
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    ip_info = ip_data()
    city = ip_info['city']
    country = ip_info['country']
    ip = ip_info['ip']

    print(current_time, city, country, ip)

    epd = epd2in13bc.EPD()
    logging.info("init and clear screen")
    epd.init()
    epd.Clear()
    time.sleep(1)

    FontFile = '/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf'
    Font25 = ImageFont.truetype(FontFile, 25)
    Font20 = ImageFont.truetype(FontFile, 20)
    Font15 = ImageFont.truetype(FontFile, 15)

    CanvasBlack = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    CanvasRed = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    drawBlack = ImageDraw.Draw(CanvasBlack)
    drawRed = ImageDraw.Draw(CanvasRed)

    drawBlack.text((5, 5), ip, font = Font25, fill = 0)
    drawRed.text((5, 40), city, font = Font20, fill = 0)
    drawRed.text((5, 60), country, font = Font15, fill = 0)
    drawBlack.text((70, 85), current_time, font = Font15, fill = 0)

    epd.display(epd.getbuffer(CanvasBlack.rotate(180)), epd.getbuffer(CanvasRed.rotate(180)))
    epd.sleep()
    epd.Dev_exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13bc.epdconfig.module_exit()
    exit()
