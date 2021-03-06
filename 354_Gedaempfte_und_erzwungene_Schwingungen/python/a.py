import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def func(t,A_0,mu):
    return A_0*np.exp(-2*np.pi*mu*t)
R = 67.2 + 50 
L = 16.87 * 10**-3
mu = R /(np.pi * 4 * L)
print(mu)
t, U =np.genfromtxt('data/a.csv', delimiter=',', unpack=True)
U = U / 80
U_1 = abs(U)
t=t/1000
plt.xlabel(r'$t \, / \, ms$')
plt.ylabel(r'$\ln \left ( U_c \,/\, U_0 \right ) $')
plt.grid()
plt.semilogx(t, U,'rx', label='Messwerte')
popt, pcov = curve_fit(func, t, U_1)
print(popt)
x=np.linspace(np.min(t), np.max(t), 100)
plt.plot(x, func(x,popt[0], popt[1]),'b-', label='Ausgleichsgrechnung')
plt.plot(x, func(x,-popt[0], popt[1]),'b-')
plt.plot(x, func(x,popt[0], mu), 'g-', label='Theoriekurve')
plt.plot(x, func(x,-popt[0], mu), 'g-', label='Theoriekurve')
plt.legend(loc='center left')
plt.savefig('plota.pdf')
plt.show()