import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.optimize import curve_fit
from uncertainties import ufloat
from scipy import stats

print('Nickel: ')
m =(18.9+ 1169.6+ 1171.8+ 520.9)/1000
F = m * 9.81 / 2#Gewichtskraft
L = 0.555 #Meter
I= 9.14*10**-10 #Meter^4

# Funktion für Curve Fit:

def D_gerade(x,a,b):
    return a*x + b

# def D_links_fit(x,E):
#     return F/(48* E * I)* (3* L**(2)*x - (4*x**3))

# def D_rechts_fit(x,E):
#     return F/(48* E * I)* ((4*x**3) - (12* L * x**2) + (9* L**2 *x) - (L**3))

# def D_Theorie(x,F,E,I,L):
#     if x <= (L/2):
#         return F/(48* E * I)* (3* L**(2)*x - (4*x**3))
#     else:
#         return F/(48* E * I)* ((4*x**3) - (12* L * x**2) + (9* L**2 *x) - (L**3))

# def D_Theorie_Array(x,F,E,I,L):
#     result = np.array([0.0]*x.size)
#     for index,xValue in enumerate(x):
#         result[index] = D_Theorie(xValue,F,E,I,L)
#         #print(D_Theorie(x[index],F,E,I,L))
#     #print(result)
#     return result

# def D_fit(x,E):
#     #x = x - b
#     if isinstance(x, (np.ndarray, np.generic) ):
#         return D_Theorie_Array(x,F,E,I,L)
#     else:
#         return D_Theorie(x,F,E,I,L)

# Daten einlesen
x,D0,DM = np.genfromtxt('data/biegung_beidseitig_eckig.csv',delimiter=',',unpack=True)

#Berechnungen
x = x*10**(-2) #m
D0 = D0*10**(-3) #m
DM = DM*10**(-3) #m
D= D0-DM #m
print(D)
x = x[2::]
D = D[2::]
# Arrays splitten
x_split = np.split(x,2)
x_links = x_split[0]
x_rechts = x_split[1]
D_split = np.split(D,2)
D_links = D_split[0]
D_rechts = D_split[1]

# Komische Achsen
x_links = (3* L**(2)*x_links - (4*x_links**3))
x_rechts = ((4*x_rechts**3) - (12* L * x_rechts**2) + (9* L**2 *x_rechts) - (L**3))

# Ausgleichskurve berechnen
params_links,pcov_links = curve_fit(D_gerade,x_links,D_links)
a_links = params_links[0]
b_links = params_links[1]
params_rechts,pcov_rechts = curve_fit(D_gerade,x_rechts,D_rechts)
a_rechts = params_rechts[0]
b_rechts = params_rechts[1]

#Fehler berechnen
a_links_err = np.absolute(pcov_links[0][0])**0.5
b_links_err = np.absolute(pcov_links[1][1])**0.5
a_rechts_err = np.absolute(pcov_rechts[0][0])**0.5
b_rechts_err = np.absolute(pcov_rechts[1][1])**0.5

#ufloats erstellen
a_links_ufloat = ufloat(a_links,a_links_err)
a_rechts_ufloat = ufloat(a_rechts,a_rechts_err)

# E berechnen
E_links = F/(48* a_links_ufloat * I)
E_rechts = F/(48* a_rechts_ufloat * I)

###########################
#linker Plot


# Plot der Ausgleichskurve
x_links_linspace = np.linspace(np.min(x_links),np.max(x_links),100)
plt.plot(x_links_linspace, D_gerade(x_links_linspace,*params_links)*10**3, 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(x_links, D_links*10**(3), 'ro', label='gemessene Auslenkung')


# Achsenbeschriftung
plt.xlabel(r'$(3 L^{2} x - (4 x^3)) \:/\: mm^3$')
plt.ylabel(r'$D \:/\: mm$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('plot_beidseitg_eckig_links.pdf')

plt.clf()

###########################
#rechter Plot

# Plot der Ausgleichskurve
x_rechts_linspace = np.linspace(np.min(x_rechts),np.max(x_rechts),100)
plt.plot(x_rechts_linspace, D_gerade(x_rechts_linspace,*params_rechts)*10**3, 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(x_rechts, D_rechts*10**(3), 'ro', label='gemessene Auslenkung')



# Achsenbeschriftung
plt.xlabel(r'$((4 x^3) - (12 L x^2) + (9 L^2 x) - (L^3)) \:/\: m^3$')
plt.ylabel(r'$D \:/\: mm$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.grid(True,which="both", linestyle='--')

# Speicherort
plt.savefig('plot_beidseitig_eckig_rechts.pdf')

print('a links: ',a_links_ufloat)
print('b links: ',b_links,'+-',b_links_err)
print('E3 links[GP]: ',E_links*10**(-9))
print('a rechts: ',a_rechts_ufloat)
print('b rechts: ',b_rechts,'+-',b_rechts_err)
print('E3 rechts[GP]: ',E_rechts*10**(-9))

# gemittelt
E_gemittelt = (E_rechts+E_links)/ 2

print('E3 gemittelt[GP]: ',E_gemittelt*10**(-9))