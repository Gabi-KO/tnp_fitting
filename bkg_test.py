import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from collections.abc import Iterable

def check_iterable(obj):
    if isinstance(obj, Iterable):
        is_iterable = True
    else:
        is_iterable = False
    
    return is_iterable

def truncate(n, decimals=0):
    multiplier = 10**decimals
    return int(n * multiplier) / multiplier

def err_exp(t):
    return np.exp(-t**2)

def bkg_func(x, *params):

    peak = params[0]
    alpha = params[1]
    beta = params[2]
    gamma = params[3]

    is_iterable = check_iterable(x)

    x0 = (alpha - x) * beta

    erfc_results = np.zeros_like(x0)
    u_results = np.zeros_like(x0)

    if is_iterable:

        for i, x0_val in enumerate(x0):
        
            # Integrate for each x0 value
            integral, _ = quad(err_exp, 0, x0_val)

            erfc_results[i] = 1 - (2 / np.sqrt(np.pi)) * integral
            u = (x[i] - peak) * gamma
            
            if u < -70:
                u_results[i] = 10**20
            elif u > 70:
                u_results[i] = 0
            else:
                u_results[i] = np.exp(-u)
    
        return erfc_results*u_results

    else:

        integral, _ = quad(err_exp, 0, x0)

        erfc = 1 - (2 / np.sqrt(np.pi)) * integral
        u0 = (x - peak) * gamma

        
        if u0 < -70:
            u = 10**20
        elif u0 > 70:
            u = 0
        else:
            u = np.exp(-u0)
        
        return erfc*u


peak = 100
alpha = 60
beta = 0.07
gamma = 0.1

p0 = (peak, alpha, beta, gamma)


#calculations at different x values

test_vals = [10, 30, 50, 60, 70, 85, 100, 125]
y_list = []
u0_list = []
x0_list = []

for i in test_vals:
    x0 = (alpha - i)*beta
    x0_list.append(x0)

    u0 = (i - peak)*gamma
    u0_list.append(u0)

    y = bkg_func(i, *p0)
    y_list.append(y)



interval = np.linspace(0, 130, 10000)

plt.plot(interval, bkg_func(interval, *p0))
plt.scatter(test_vals, y_list)

for i in range(len(test_vals)):
    x = test_vals[i]
    y = y_list[i]

    y_p = truncate(y, 3)
    
    plt.annotate(f'({x}, {y_p})', xy=(x - 10,y), xytext=(10,10), textcoords='offset points')

    print(f'({x}, {y_p})')
    print(f'u0 = {u0_list[i]}')
    print(f'x0 = {x0_list[i]}')

plt.show()
