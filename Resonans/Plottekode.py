import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_impedans(filnavn, resonansfrekvens=None):
    # Leser csv-fil
    df = pd.read_csv(filnavn)

    # Henter spenning og frekvens
    frekvens = df["F"]  # Frekvens i Hz
    spenning = (df["V_inn"] - df["V_ut"]) / df["V_ut"]  # Vmath/Vc2
    ch1 = df["V_inn"]
    ch2 = df["V_ut"]

    # Verdier
    R = 1.0014 * 10**3
    C = 10.1e-9
    L = 4.7e-3

    # Regner ut Z
    impedans = spenning * R

    # Beregner f0
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))

    # Usikkerhet
    d2 = 5 / 100
    dm = 5 / 100 + 4 / 100
    dR = 0.005 * 1e3
    dC = 0.7e-9
    dL = 0.1e-3
    dF = frekvens * 1 / 100 

    # Regner ut feil
    dz = impedans * (d2 / ch2 + dm / abs(ch1 - ch2) + dR / R)
    df0 = f0 / 2 * (dC / C + dL / L)

    # Plotter med error bars
    plt.figure(figsize=(8, 6))
    plt.errorbar(frekvens, impedans, yerr=dz, xerr=dF, fmt="o", color="b", linestyle="",
                 ecolor="orange", capsize=5, elinewidth=1.5, label="|Z| mot Frekvens")
    
    # Plott resonansfrekvens (enten fra input eller beregnet verdi)
    if resonansfrekvens is None:
        resonansfrekvens = f0

    plt.axvline(x=resonansfrekvens, color='red', linestyle="--", label=f'Resonansfrekvens: {resonansfrekvens:.0f} Hz')
    plt.axvline(x=resonansfrekvens + df0, color='purple', linestyle="--", alpha=0.5)
    plt.axvline(x=resonansfrekvens - df0, color='purple', linestyle="--", alpha=0.5, label=f'Usikkerhet: ±{df0:.0f} Hz')

    # Akse-labels og tittel
    plt.xlabel("Frekvens (Hz)")
    plt.ylabel("Impedans |Z| (Ω)")
    if filnavn=="oppg1b.csv":
        plt.title("Impedans mot Frekvens-Parallell svingekrets")
    else:
        plt.title("Impedans mot Frekvens-Serie svingekrets")
    # Grid og legend
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.show()


# Kall funksjonen for de to datasettene
plot_impedans("oppg1b.csv")
plot_impedans("oppg2c.csv", resonansfrekvens=23.57e3)
