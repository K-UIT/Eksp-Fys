import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.linear_model import LinearRegression

def analyser_og_plotte(filnavn, label):
    # Leser inn data fra Excel-filen
    data = pd.read_excel(filnavn, header=None).to_numpy()[1:]

    # Antall målinger
    n = data.shape[0]

    # Temperatur og spenning som lister
    temperatur = data[:, 0]
    spenning = data[:, 1]

    # Lineær tilpasning
    # Regner ut summer
    sx = np.sum(temperatur)
    sx2 = np.sum(temperatur**2)
    sy = np.sum(spenning)
    sxy = np.sum(temperatur * spenning)
    # Regner ut A og B
    A = (n * sxy - sx * sy) / (n * sx2 - sx**2)
    B = (sy - A * sx) / n

    spenning_hat = A * temperatur + B
    SSE_lin = np.sum((spenning - spenning_hat) ** 2)

    # Usikkerhet
    sigma_y = sqrt(SSE_lin / (n - 2))
    sigma_A = sigma_y * sqrt(sx2 / (n * sx2 - sx**2))
    sigma_B = sigma_y * sqrt(n / (n * sx2 - sx**2))

    print(f"{label} - Lineær tilpasning:")
    print(f"A = {A:.5f}, B = {B:.5f}")
    print(f"SSE (lineær): {SSE_lin:.5f}")
    print(f"Usikkerhet: sigma_A = {sigma_A:.5f}, sigma_B = {sigma_B:.5f}")

    # Kvadratisk tilpasning
    xq = np.column_stack((temperatur**2, temperatur))
    kvadratisk_modell = LinearRegression().fit(xq, spenning)

    # Koeffisienter
    C, A_kvadratisk = kvadratisk_modell.coef_  # C for x^2, A_kvadratisk for x
    B_kvadratisk = kvadratisk_modell.intercept_

    spenning_Qhat = kvadratisk_modell.predict(xq)
    SSE_kvadratisk = np.sum((spenning - spenning_Qhat) ** 2)

    print(f"{label} - Kvadratisk tilpasning:")
    print(f"A = {A_kvadratisk:.5f}, B = {B_kvadratisk:.5f}, C = {C:.5f}")
    print(f"SSE (kvadratisk): {SSE_kvadratisk:.5f}")
    print(f"Forskjell i SSE: {abs(SSE_lin - SSE_kvadratisk):.5f}")
    print("-" * 40)

    return temperatur, spenning, spenning_hat, spenning_Qhat, round(A, 2), round(B, 2), round(A_kvadratisk, 2), round(B_kvadratisk, 2), round(C, 5), sigma_y

# Henter data for begge forsøk
temp1, spenning1, spenning_hat1, spenning_Qhat1, A1, B1, A1_kv, B1_kv, C1, sigma1 = analyser_og_plotte("Run 1.xlsx", "Forsøk 1")
temp2, spenning2, spenning_hat2, spenning_Qhat2, A2, B2, A2_kv, B2_kv, C2, sigma2 = analyser_og_plotte("Run 2.xlsx", "Forsøk 2")

# === FIGUR 1: LINEÆR TILPASNING ===
figur1, akser1 = plt.subplots(1, 2, figsize=(12, 5))

# Forsøk 1 - Lineær
akser1[0].scatter(temp1, spenning1, color="blue", label="Måledata")
akser1[0].plot(temp1, spenning_hat1, color="red", label=f"Lineær: y = {A1}x {B1}")
akser1[0].plot(temp1, spenning_hat1+sigma1, color="yellow", linestyle="--", label="Usikkerhet ±{round(sigma1,2)}")
akser1[0].plot(temp1, spenning_hat1-sigma1, color="yellow", linestyle="--")
akser1[0].set_title("Lineær Tilpasning - Forsøk 1")
akser1[0].set_xlabel("Temperatur (°C)")
akser1[0].set_ylabel("Spenning (mV)")
akser1[0].legend()
akser1[0].grid()

# Forsøk 2 - Lineær
akser1[1].scatter(temp2, spenning2, color="green", label="Måledata")
akser1[1].plot(temp2, spenning_hat2, color="purple", label=f"Lineær: y = {A2}x {B2}")
akser1[1].plot(temp2, spenning_hat2+sigma2, color="orange", linestyle="--", label=f"Usikkerhet ±{round(sigma2,2)}")
akser1[1].plot(temp2, spenning_hat2-sigma2, color="orange", linestyle="--")
akser1[1].set_title("Lineær Tilpasning - Forsøk 2")
akser1[1].set_xlabel("Temperatur (°C)")
akser1[1].set_ylabel("Spenning (mV)")
akser1[1].legend()
akser1[1].grid()

plt.tight_layout()
plt.show()

# === FIGUR 2: KVADRATISK TILPASNING ===
figur2, akser2 = plt.subplots(1, 2, figsize=(12, 5))

# Forsøk 1 - Kvadratisk
akser2[0].scatter(temp1, spenning1, color="blue", label="Måledata")
akser2[0].plot(temp1, spenning_Qhat1, color="yellow", label=f"Kvadratisk: y = {C1}x² + {A1_kv}x {B1_kv}")
akser2[0].set_title("Kvadratisk Tilpasning - Forsøk 1")
akser2[0].set_xlabel("Temperatur (°C)")
akser2[0].set_ylabel("Spenning (mV)")
akser2[0].legend()
akser2[0].grid()

# Forsøk 2 - Kvadratisk
akser2[1].scatter(temp2, spenning2, color="green", label="Måledata")
akser2[1].plot(temp2, spenning_Qhat2, color="orange", label=f"Kvadratisk: y = {C2}x² + {A2_kv}x {B2_kv}")
akser2[1].set_title("Kvadratisk Tilpasning - Forsøk 2")
akser2[1].set_xlabel("Temperatur (°C)")
akser2[1].set_ylabel("Spenning (mV)")
akser2[1].legend()
akser2[1].grid()

plt.tight_layout()
plt.show()
