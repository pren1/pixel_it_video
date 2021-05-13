colors = [
    [140, 143, 174],
    [88, 69, 99],
    [62, 33, 55],
    # [154, 99, 72], # orange
    [215, 155, 125],
    [245, 237, 186],
    [192, 199, 65],
    [100, 125, 52],
    [228, 148, 58],
    [157, 48, 59],
    [210, 100, 113],
    [112, 55, 127],
    [126, 196, 193],
    [52, 133, 157],
    [23, 67, 75],
    [31, 14, 28],
  ]

import numpy as np
import matplotlib.pyplot as plt
import pdb
from skimage import io
palette = np.asarray(colors)
m = 16
n = 1
indices = np.asarray([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15]])
print(indices)
io.imshow(palette[indices])
