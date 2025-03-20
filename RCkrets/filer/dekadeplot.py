import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Les inn data fra CSV 
filename = "lowpass_characterisation.csv" 

data = pd.read_csv(filename)

# Leser av "Frekvens", "Vinn", "Vut", "Faseforskjell"
frekvens = data["F"]
vinn = data["V_inn"]
vut = data["V_ut"]
faseforskjell = data["phase"]

# Beregn forsterkning (Vut/Vin) og konverter til desibel (dB)
forsterkning_db = 20 * np.log10(vut / vinn)

# Finn verdiene for forsterkning i dB ved f = 10^4 Hz og f = 10^5 Hz
f_10kHz = 10**4
f_100kHz = 10**5

# Finn indekser for de ønskede frekvensene
idx_10kHz = np.argmin(np.abs(frekvens - f_10kHz))
idx_100kHz = np.argmin(np.abs(frekvens - f_100kHz))

# Hent forsterkning i dB ved de to frekvensene
forsterkning_db_10kHz = forsterkning_db[idx_10kHz]
forsterkning_db_100kHz = forsterkning_db[idx_100kHz]

# Beregn forskjellen i dB mellom de to frekvensene
delta_db = forsterkning_db_100kHz - forsterkning_db_10kHz

# Skriv ut resultatet
print(f"Forsterkning ved 10 kHz: {forsterkning_db_10kHz:.2f} dB")
print(f"Forsterkning ved 100 kHz: {forsterkning_db_100kHz:.2f} dB")
print(f"Forskjell i dB mellom 10 kHz og 100 kHz: {delta_db:.2f} dB")

# Visualiser resultatet i en graf
plt.figure(figsize=(8, 4))
plt.semilogx(frekvens, forsterkning_db, label="Amplitudekarakteristikk (dB)")
plt.axvline(f_10kHz, color='r', linestyle='--', label="10 kHz")
plt.axvline(f_100kHz, color='b', linestyle='--', label="100 kHz")
plt.xlabel("Frekvens (Hz)")
plt.ylabel("Forsterkning (dB)")
plt.title("Amplitudekarakteristikk og Forskjell i dB mellom 10 kHz og 100 kHz")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
