#!/usr/bin/env python3

# get 100 random images from http://lorempixel.com/

import os
import time
import timeit
# import hashlib  # may be to be done ... check that every image has a different hash.
import requests
from PIL import Image
from io import BytesIO
from multiprocessing import Pool

DIMENSIONS = ((300, 300), (100, 100), (20, 20))  # Largest has better to be 1st

# Parallelize download into 10 pools of 10 downloads
NB_POOLS = 10
IMAGES_PER_POOL = 10

PROJDIR = os.path.dirname(os.path.dirname(__file__))

def pool_job(job_num):
    for img_num in range(IMAGES_PER_POOL):
        img = None
        for width, height in DIMENSIONS:
            if img is None:
                while True:
                    try:
                        url = "http://lorempixel.com/{}/{}".format(width, height)
                        response = requests.get(url)
                        img = Image.open(BytesIO(response.content))
                        break
                    except Exception as e:
                        print("Exception while downloading an image : {}.\nRetry in 1s.".format(e))
                        time.sleep(1)
            thumb_img = img.copy()
            thumb_img.thumbnail((width, height))
            thumb_img.save(os.path.join(PROJDIR, "data/images/{}_{}/{:03d}.jpg".format(width, height, job_num * IMAGES_PER_POOL + img_num)))

for dim in DIMENSIONS:
    os.makedirs(os.path.join(PROJDIR, "data/images/{}_{}".format(dim[0], dim[1])), exist_ok=True)

def main():
    with Pool(NB_POOLS) as p:
        p.map(pool_job, range(NB_POOLS))

if __name__ == "__main__":
    chrono = timeit.timeit("main()", number=1, setup="from __main__ import main")
    print("Completed to download {} x {} images from http://lorempixel.com/ in {} seconds".format(NB_POOLS, IMAGES_PER_POOL, chrono))
