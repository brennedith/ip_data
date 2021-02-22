#!/usr/bin/python3

import os
import sys
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import time
import json
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13bc

logging.basicConfig(level=logging.DEBUG)

# IP Data Logic
def ip_data():
    ip_data_provider = 'https://api-ipv4.ip.sb/geoip'
    interface = 'wlan0'
    cmd = ' '.join([
        'curl',
        '--silent',
        '--show-error',
        # OpenVPN interface
        '--interface',
        interface,
        ip_data_provider
    ])

    ip_data_request = os.popen(cmd)
    ip_data_response = ip_data_request.read()
    ip_data_json = json.loads(ip_data_response)

    return ip_data_json

try:
    epd = epd2in13bc.EPD()
    logging.info("init and clear screen")
    epd.init()
    epd.Clear()
    time.sleep(1)

    #FontFile = os.path.join(picdir, 'Font.ttc')
    FontFile = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
    Font25 = ImageFont.truetype(FontFile, 25)
    Font20 = ImageFont.truetype(FontFile, 20)
    Font15 = ImageFont.truetype(FontFile, 15)

    CanvasBlack = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    CanvasRed = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    drawBlack = ImageDraw.Draw(CanvasBlack)
    drawRed = ImageDraw.Draw(CanvasRed)

    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    ip_info = ip_data()
    city = ip_info['city']
    country = ip_info['country']
    ip = ip_info['ip']

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
