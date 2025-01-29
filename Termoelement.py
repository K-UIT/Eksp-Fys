import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


# Leser excel filen
data = pd.read_excel("Run 2.xlsx", header=None)

data = data.to_numpy()
data = data[1:]

# Antall målinger
n = data.shape[0]

# Temperatur og volt som lister, skalerer også volten
Temp = data[:, 0]
Volt = data[:, 1]

# Lineær

# Regner ut summer
sx = np.sum(Temp)
sx2 = np.sum(Temp**2)
sy = np.sum(Volt)
sxy = np.sum(Temp*Volt)

# Regner ut A og B
A = (n*sxy-sx*sy)/(n*sx2-sx**2)

B = (sy-A*sx)/n

Volt_hat = A*Temp+B

SSE_lin = np.sum((Volt-Volt_hat)**2)
print("SSE for lineær tilpassing",SSE_lin)


# Regner usikkerhet
Sigmay = sqrt(SSE_lin/(n-2))

SigmaA = Sigmay*sqrt(sx2/(n*sx2-(sx)**2))
SigmaB = Sigmay*sqrt(n/(n*sx2-(sx)**2))

print("Usikkerhet for A er: ", SigmaA)
print("Usikkerhet for B er: ", SigmaB)
print("Usikkerhet for målt verdi: ", Sigmay)

# Plotting
plt.scatter(Temp, Volt, color="blue", label="Data")
plt.plot(Temp, A * Temp + B + Sigmay, color="yellow", linestyle="--")
plt.plot(Temp, A * Temp + B - Sigmay, color="yellow", linestyle="--", label="Usikkerhet")
plt.plot(Temp, A * Temp + B, color="red", label=f"Lineær: y = {A:.2f}x {B:.2f}")
plt.xlabel("Temperatur (°C)")
plt.ylabel("Volt (mV)")
plt.legend()
plt.grid()
plt.show()

# Quadratic
from sklearn.linear_model import LinearRegression

# Lager en matrise med X^2 og X
xq = np.column_stack((Temp**2, Temp))

# Lager en annen ordens model
quad_model = LinearRegression().fit(xq, Volt)

# Lager y hat
Volt_Qhat = quad_model.predict(xq)

# Plotting
plt.scatter(Temp, Volt, color="blue", label="Data")
plt.plot(Temp, Volt_Qhat, label="Quadratic Fit", color="yellow")
plt.plot(Temp, A * Temp + B, color="red", label=f"Lineær: y = {A:.2f}x {B:.2f}")
plt.xlabel("Temperatur (°C)")
plt.ylabel("Volt (mV)")
plt.legend()
plt.grid()
plt.show()

SSE_quad = np.sum((Volt - Volt_Qhat)**2)

print(f"Linear SSE: {SSE_lin}")
print(f"Quadratic SSE: {SSE_quad}")
print("Forskjell: ",abs(SSE_lin-SSE_quad))
