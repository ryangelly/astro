import os

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

    with multiprocessing.Pool(processes=2) as pool: 
        results = pool.map(worker_function, dirlist)

    for result in results:
        average += result

    print(np.max(average))

    maxval = np.max(average)
    minval = np.min(average)
    print(maxval, minval)
    average = np.array(2**15 * (average-minval)/(maxval-minval), np.uint16)
    print(average)

# rgb = None


#         if rgb is None:
#             rgb = np.array(raw.postprocess(output_bps=16))
#             average = np.zeros(rgb.shape, np.float32)
#             average += rgb
#         else:
#             rgb = np.array(raw.postprocess(output_bps=16))
#             average += rgb
#     print(average)

# print(np.max(average))

# maxval = np.max(average)
# minval = np.min(average)
# print(maxval, minval)
# average = np.array(2**15 * (average-minval)/(maxval-minval), np.uint16)
# print(average)
# imageio.imsave('default.tiff', average)