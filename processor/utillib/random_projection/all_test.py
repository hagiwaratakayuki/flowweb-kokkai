from utillib.random_projection import projection
import numpy as np
DUMMY_ARR = np.zeros((10, 300), dtype=float)
print(projection(DUMMY_ARR).shape)
