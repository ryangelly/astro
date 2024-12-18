import os

import rawpy
import numpy as np
import imageio

directory = 'test_images'

rgb = None

for fn in os.listdir(directory):
    fp = os.path.join(directory,fn)
    if os.path.isfile(fp):
        print(fn)
        raw = rawpy.imread(fp)
        if rgb is None:
            rgb = np.array(raw.postprocess(output_bps=16))
            average = np.zeros(rgb.shape, np.float32)
            average += rgb
        else:
            rgb = np.array(raw.postprocess(output_bps=16))
            average += rgb
    print(average)

print(np.max(average))

maxval = np.max(average)
minval = np.min(average)
print(maxval, minval)
average = np.array(2**15 * (average-minval)/(maxval-minval), np.uint16)
print(average)
imageio.imsave('default.tiff', average)