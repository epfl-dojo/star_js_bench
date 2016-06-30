#!/usr/bin/env python3

"""
Get 100 random unique images from https://unsplash.it/
"""

import os
import time
import timeit
import hashlib
from io import BytesIO
from PIL import Image
from multiprocessing import Process, Lock, Manager
import requests

DIMENSIONS = ((800, 800), (300, 300), (100, 100), (20, 20))  # Largest has better to be 1st

# Parallelize download into 10 pools of 10 downloads
NB_POOLS = 10
IMAGES_PER_POOL = 10

PROJDIR = os.path.dirname(os.path.dirname(__file__))

def get_hash(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

def process_job(job_num, shared_namespace):
    """
    Download, resize and save IMAGES_PER_POOL unique images
    """
    def check_unique(one_hash):
        """
        Check in shared namespace that that hash doesn't exist
        """
        with lock:
            if one_hash not in shared_namespace.hashes:
                list_hashes = shared_namespace.hashes
                list_hashes.append(one_hash)
                shared_namespace.hashes = list_hashes
                return True
            else:
                return False

    for img_num in range(IMAGES_PER_POOL):
        img = None
        for width, height in DIMENSIONS:
            if img is None:
                while True:
                    try:
                        url = "https://unsplash.it/{}/{}/?random".format(width, height)
                        response = requests.get(url)
                        if check_unique(get_hash(response.content)):
                            img = Image.open(BytesIO(response.content))
                            break
                        else:
                            print("Downloaded an image that we already have, retrying...")
                    except Exception as e:
                        print("Exception while downloading an image : {}.\nRetry in 1s.".format(e))
                        time.sleep(1)
            thumb_img = img.copy()
            thumb_img.thumbnail((width, height))
            thumb_img.save(os.path.join(PROJDIR, "data/images/{}_{}/{:03d}.jpg".format(width, height, job_num * IMAGES_PER_POOL + img_num)))

def main():
    processes = []
    manager = Manager()
    shared_namespace = manager.Namespace()
    shared_namespace.hashes = []
    for i in range(NB_POOLS):
        proc = Process(target=process_job, args=(i, shared_namespace))
        proc.start()
        processes.append(proc)
    for proc in processes:
        proc.join()

if __name__ == "__main__":
    lock = Lock()
    for dim in DIMENSIONS:
        os.makedirs(os.path.join(PROJDIR, "data/images/{}_{}".format(dim[0], dim[1])), exist_ok=True)

    chrono = timeit.timeit("main()", number=1, setup="from __main__ import main")
    print("Completed to download {} x {} images from https://unsplash.it/ in {} seconds".format(NB_POOLS, IMAGES_PER_POOL, chrono))
