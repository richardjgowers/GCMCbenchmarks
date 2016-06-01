"""Functions for defining the decorrelation time of a signal

"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from statsmodels.tsa import stattools


def grab_until(sig, thresh):
    """Works on falling signals"""
    # find index where signal is first below value
    cut = sig[sig < thresh].index[0]

    return sig[:cut].iloc[:-1]  # return signal up to cut, excluding cut

def grab_after(sig, thresh):
    """Works on falling signals"""
    cut = sig[sig < thresh].index[0]
    
    return sig[cut:]

def exp_fit(x, tau):
    return np.exp(-x/tau)

def do_exp_fit(sig, thresh=0.1):
    """Fit an exponential up to thresh

    Single exponential::
      y = exp(-x/tau)

    Parameters
    ----------
    sig : pd.Series
      timeseries of the signal
    thresh : float, optional
      value at which to cut off the signal when fitting

    Returns
    -------
    coefficient for tau
    """
    sig = grab_until(sig, thresh)
    # grab sig up to where it first goes below threshhold
    
    x, y = sig.index, sig.values
    return curve_fit(exp_fit, x, y, p0=10000)[0][0]

def find_tau(sig, eq, tmax=5000000, thresh=0.1):
    """
    Parameters
    ----------
    sig : pd.Series
      the entire signal, including equilibrium phase
    eq : int
      the number of steps before equilibration
    tmax : int, optional
      the total number of steps to calculate the autocorrelation for
    thresh : float, optional
      Value until which the ACF is fitted to [Default: 0.1]
    """
    # find how many rows of sig we will use
    nlags = sig[:tmax].shape[0]
    acf = stattools.acf(sig[eq:], fft=True, nlags=nlags)
    # +1 as acf at zero is returned
    acf = pd.Series(acf, sig.index[:nlags + 1])

    return do_exp_fit(acf, thresh=thresh)
