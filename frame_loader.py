import os
import time

import rawpy
import numpy as np
import imageio

import multiprocessing

def worker_function(fn):
    # Your function to be executed in parallel
    directory = 'test_images'
    fp = os.path.join(directory,fn)
    if os.path.isfile(fp):
        print(fn)
        raw = rawpy.imread(fp)
        return np.array(raw.postprocess(output_bps=16))


if __name__ == '__main__':
    directory = 'test_images'
    dirlist = os.listdir(directory)

    fn = dirlist[0]
    fp = os.path.join(directory,fn)
    if os.path.isfile(fp):
        print(fn)
        raw = rawpy.imread(fp)

    rgb = np.array(raw.postprocess(output_bps=16))
    average = np.zeros(rgb.shape, np.float32)

    start_time = time.time()

    with multiprocessing.Pool(processes=4) as pool: 
        results = pool.map(worker_function, dirlist)

    for result in results:
        average += result

    end_time = time.time()

    elapsed_time = end_time - start_time

    print("Elapsed time:", elapsed_time, "seconds")

    print(np.max(average))

    maxval = np.max(average)
    minval = np.min(average)
    print(maxval, minval)
    average = np.array(2**15 * (average-minval)/(maxval-minval), np.uint16)
    print(average)

