# Probability Distribution Function
#
# Based on https://arxiv.org/pdf/cond-mat/0507657.pdf

import numpy as np

from typing import Callable, Any

from math import exp
from scipy.integrate import quad_vec as integrate

def create_pdf(T: float, __lambda: Callable[[float], float]) -> Callable[[float], float]:
    """
    Create a pdf of inter-arrival time.

    T is the difference of start time and end time.
    _lambda is the function for mean number of occurence.

    For more details, read the document from the link at
    the top of this file
    """
    def pdf(x: float) -> float:
        """
        Probability function from time 0 to T
        """
        
        __upcase_lambda: Callable[[float], Any] = lambda t: integrate(__lambda, 0, t)[0]
        
        __fst_diff = lambda y: __lambda(y) * __lambda(y + x) * np.exp(
            - ( __upcase_lambda(y + x) - __upcase_lambda(y) )
        )
        
        __fst = (1 / __upcase_lambda(T)) * integrate(__fst_diff, 0, T - x)[0]
        __snd = ( __lambda(x) * exp( - __upcase_lambda(x)) ) / __upcase_lambda(T)

        return __fst + __snd

    return pdf