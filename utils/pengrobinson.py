import numpy as np
from scipy.constants import R  # gas constant


def calc_A(P, T, Pc, Tc, omega):
    ret = P / R**2 / T**2
    ret *= 0.47724 * R**2 * Tc ** 2 / Pc

    Tr = T / Tc
    kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega ** 2
    alpha = (1 + kappa * (1 - Tr**0.5))**2    
    
    ret *= alpha
    
    return ret


def calc_B(P, T, Pc, Tc):
    ret = P / R / T
    b = 0.077796 * R * Tc / Pc
    ret *= b
    
    return ret


def find_Z(P, T, Pc, Tc, omega):
    """Find compressibility factor from cubic expression"""
    A = calc_A(P, T, Pc, Tc, omega)
    B = calc_B(P, T, Pc, Tc)

    # Coefficients for the cubic expression of Z
    rts = np.roots(np.array([1,  # Z**3
                             B-1,   # Z**2
                             A - 3 * B**2 - 2*B,  # Z
                             B**3 + B**2 - A*B]))  # 1
    # Return the first real root, should only be one?
    return [r for r in rts if np.isreal(r)][0].real


def calc_fugacity_coeff(P, T, Pc, Tc, omega):
    """Find the fugacity coefficient

    P, Pc
      system pressure and critical pressure in Pa
    T, Tc
      system temperature and critical temperature in K
    omega
      acentric factor
    """
    ln = np.log
    A = calc_A(P, T, Pc, Tc, omega)
    B = calc_B(P, T, Pc, Tc)
    Z = find_Z(P, T, Pc, Tc, omega)
    rt2 = np.sqrt(2)

    lnP = Z - 1 
    lnP -= ln(Z - B) 
    lnP -=  A/(2 * rt2 * B) * ln((Z + (1 + rt2) * B)/(Z + (1 - rt2) * B))

    return np.exp(lnP)
