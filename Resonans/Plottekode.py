import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def beregn_impedans(filnavn):
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
    df0 = f0 * (dC / C + dL / L) / 2

    return frekvens, impedans, dz, dF, f0, df0

def plot_impedans(filnavn, rf=None):
    # Beregn impedans og usikkerhet
    frekvens, impedans, dz, dF, f0, df0 = beregn_impedans(filnavn)

    # Plotter med error bars
    plt.figure(figsize=(8, 6))
    plt.errorbar(frekvens, impedans, yerr=dz, xerr=dF, fmt="o", color="b", linestyle="",
                 ecolor="orange", capsize=5, elinewidth=1.5, label="Målte verdier")

    # Plott resonansfrekvens (enten fra input eller beregnet verdi)
    if rf is None:
        rf = f0

    plt.axvline(x=rf, color='red', linestyle="--", label=f'Målt resonansfrekvens: {rf:.0f} Hz')

    # Akse-labels og tittel
    plt.xlabel("Frekvens (Hz)")
    plt.ylabel("Impedans |Z| (Ω)")
    if filnavn == "oppg1b.csv":
        plt.title("Impedans mot Frekvens - Parallell svingekrets")
    else:
        plt.title("Impedans mot Frekvens - Serie svingekrets")
    
    # Grid og legend
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.show()

    # Returnere f0 og df0 for videre bruk
    return f0, df0


# Kall funksjonen for de to datasettene og returner f0 og df0
plot_impedans("oppg1b.csv", 23.54e3)
f0, df0 = plot_impedans("oppg2c.csv", 23.57e3)

# Verdier
x = [0, 1, 2]  # X-aksen: 0 for Teoretisk, 1 for Parallell, 2 for Serie
y = [f0, 23.54e3, 23.57e3]  # Y-aksen: f0, parallell resonansfrekvens og serie resonansfrekvens
yerror = [df0, 200, 200]  # Feilmargene for de forskjellige frekvensene

# Plotting
plt.figure(figsize=(8, 6))

# Feilplott med rød for teoretisk verdi og blå for parallell og serie
plt.errorbar(x[0], y[0], yerr=yerror[0], fmt="o", color="red",capsize=5, elinewidth=1.5, label="Teoretisk resonans")
plt.errorbar(x[1], y[1], yerr=yerror[1], fmt="o", color="blue",capsize=5, elinewidth=1.5, label="Parallell resonans")
plt.errorbar(x[2], y[2], yerr=yerror[2], fmt="o", color="purple",capsize=5, elinewidth=1.5, label="Serie resonans")

# Tilpasse x-aksen etiketter
plt.xticks(x, ["Teoretisk", "Parallell", "Serie"])

# Legge til etiketter og tittel
plt.xlabel("Krets")
plt.ylabel("Frekvens (Hz)")
plt.title("Resonansfrekvenser med usikkerhet")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.show()
