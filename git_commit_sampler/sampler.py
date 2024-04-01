# Rejection Sampling

import numpy as np

from typing import Callable

def rejection_sample(pdf: Callable[[float], float], M: float, T: float):
    rn_x = np.random.uniform(0, T)
    rn_y = np.random.uniform(0, M)
    threshold = pdf(rn_x)
    while rn_y > threshold:
        rn_x = np.random.uniform(0, T)
        rn_y = np.random.uniform(0, M)
        threshold = pdf(rn_x)
        # print(f"rn_x: {rn_x}, rn_y: {rn_y}, threshold, {threshold}")

    return rn_x