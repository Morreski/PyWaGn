#!/usr/bin/python3

import urllib.request
import random
import sys
import os
import tempfile
import subprocess

from bs4 import BeautifulSoup
import begin

SHELL_COMMAND = "gsettings set org.gnome.desktop.background picture-uri file://{path}"
WALLPAPER_DIR = "~/Pictures/"


def get_random_image_url(image_range):
    # Build request with dummy user agent (avoid being kickbanned)
    request = urllib.request.Request("https://www.reddit.com/r/wallpaper/?count=0&limit=%s" % image_range, headers={'User-Agent': 'Wololo'})
    response = urllib.request.urlopen(request)

    # Get /r/wallpaper content
    soup = BeautifulSoup(response.read().decode("utf-8"), "lxml")
    links = soup.findAll('a', {'class': 'title may-blank '})

    if not links:
        print("No image found")
        sys.exit(1)

    random.shuffle(links)
    return links[0]['href']


def get_file_from_url(url):
    image = urllib.request.urlopen(url).read()
    root_dir = os.path.expanduser(WALLPAPER_DIR)
    f = open(os.path.join(root_dir, "wallpaper"), 'wb')
    f.write(image)
    return f


@begin.start
def run(image_range=25):
    print("Picking random image.")
    image_url = get_random_image_url(image_range)
    print("Found %s, downloading..." % image_url)
    image_file = get_file_from_url(image_url)
    process = subprocess.Popen(SHELL_COMMAND.format(path=image_file.name), shell=True)
    process.wait()
    print("Done !")
