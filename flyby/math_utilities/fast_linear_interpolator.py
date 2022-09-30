from numba import njit
import numpy as np


@njit
def lerp_numba(arr: np.ndarray, jd: np.ndarray, jd_eval: float) -> np.ndarray:
    '''
    Return the linear interpolation of the array at the specified julian date

    Parameters
    ----------
    arr : np.ndarray
        The array to interpolate, of shape (n, 3)
    jd : np.ndarray
        The julian dates corresponding to the values in arr
    jd_eval : float
        The julian date at which to evaluate the interpolation

    Returns
    -------
    np.ndarray
        The interpolated array
    '''
    # Find the index of the first element in the array that is greater than the evaluation time
    i = np.searchsorted(jd, jd_eval)

    # If the evaluation time is less than the first element in the array, return the first element
    if i == 0:
        return arr[0]

    # If the evaluation time is greater than the last element in the array, return the last element
    if i == len(jd):
        return arr[-1]

    # If the evaluation time is between two elements, interpolate between the two elements
    return arr[i - 1] + (arr[i] - arr[i - 1]) * (jd_eval - jd[i - 1]) / (jd[i] - jd[i - 1])


class FastLerp:
    '''
    Limitation: can only evaluate at a single time
    '''

    def __init__(self, jd: np.ndarray, arr: np.ndarray):
        self.arr = arr.T
        self.jd = jd

    def __call__(self, jd_eval: float):
        return lerp_numba(self.arr, self.jd, jd_eval)
