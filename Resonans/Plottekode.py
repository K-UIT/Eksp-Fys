import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def beregn_impedans(filnavn):
    df = pd.read_csv(filnavn)

    # Leser av data
    frekvens = df["F"]  
    spenning = (df["V_inn"] - df["V_ut"]) / df["V_ut"] 
    ch1 = df["V_inn"]
    ch2 = df["V_ut"]

    # Definerer konstanter
    R = 1.0014 * 10**3
    C = 10.1e-9
    L = 4.7e-3

    # Regner ut impedans
    impedans = spenning * R

    # Regner ut teoretisk resonansfrekvens
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    # Definerer usikkerheter
    d2 = 5 / 100
    dm = 5 / 100 + 4 / 100
    dR = 0.005 * 1e3
    dC = 0.7e-9
    dL = 0.1e-3
    dF = frekvens * 1 / 100 
    # Regner ut usikkerheter
    dz = impedans * (d2 / ch2 + dm / abs(ch1 - ch2) + dR / R)
    df0 = f0 * (dC / C + dL / L) / 2

    return frekvens, impedans, dz, dF, f0, df0

# Opprett figur med to subplots
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Parallellkrets på første subplot
ax1 = axes[0]
frekvens_p, impedans_p, dz_p, dF_p, f0_p, df0_p = beregn_impedans("oppg1b.csv")
ax1.errorbar(frekvens_p, impedans_p, yerr=dz_p, xerr=dF_p, fmt="o", color="b", linestyle="",
             ecolor="orange", capsize=5, elinewidth=1.5, label="Parallell svingekrets")
ax1.axvline(x=23.54e3, color='red', linestyle="--", label=f'Parallell resonans: {23.54e3:.0f} Hz')
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel("Frekvens (Hz)")
ax1.set_ylabel("Impedans |Z| (Ω)")
ax1.set_title("Impedans mot Frekvens - Parallell svingekrets")
ax1.grid(True, which="both", linestyle="--", linewidth=0.5)
ax1.legend()

# Seriekrets på andre subplot
ax2 = axes[1]
frekvens_s, impedans_s, dz_s, dF_s, f0_s, df0_s = beregn_impedans("oppg2c.csv")
ax2.errorbar(frekvens_s, impedans_s, yerr=dz_s, xerr=dF_s, fmt="o", color="purple", linestyle="",
             ecolor="green", capsize=5, elinewidth=1.5, label="Serie svingekrets")
ax2.axvline(x=23.57e3, color='red', linestyle="--", label=f'Serie resonans: {23.57e3:.0f} Hz')
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel("Frekvens (Hz)")
ax2.set_ylabel("Impedans |Z| (Ω)")
ax2.set_title("Impedans mot Frekvens - Serie svingekrets")
ax2.grid(True, which="both", linestyle="--", linewidth=0.5)
ax2.legend()

plt.tight_layout()
plt.show()

# Plot for resonansfrekvenser
x = [0, 1, 2]
y = [f0_p, 23.54e3, 23.57e3]  
yerror = [df0_p, 200, 200]

plt.figure(figsize=(8, 6))
plt.errorbar(x[0], y[0], yerr=yerror[0], fmt="o", color="red", capsize=5, elinewidth=1.5, label="Teoretisk resonans")
plt.errorbar(x[1], y[1], yerr=yerror[1], fmt="o", color="blue", capsize=5, elinewidth=1.5, label="Parallell resonans")
plt.errorbar(x[2], y[2], yerr=yerror[2], fmt="o", color="purple", capsize=5, elinewidth=1.5, label="Serie resonans")
plt.xticks(x, ["Teoretisk", "Parallell", "Serie"])
plt.xlabel("Krets")
plt.ylabel("Frekvens (Hz)")
plt.title("Resonansfrekvenser med usikkerhet")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.show()
