import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Les inn data fra CSV (endre filnavn hvis nødvendig)
filename = "lowpass_characterisation.csv"  # Sett inn riktig filnavn

data = pd.read_csv(filename)

# Anta at CSV-fila har kolonnene: "Frekvens", "Vinn", "Vut", "Faseforskjell"
frekvens = data["F"]
vinn = data["V_inn"]
vut = data["V_ut"]
faseforskjell = data["phase"]

# Beregn forsterkning (Vout/Vin)
forsterkning = vut / vinn

# Finn grensefrekvensen (der forsterkning faller til 1/√2)
idx_f0 = np.where(forsterkning <= 1/np.sqrt(2))[0][0]  # Første punkt under 1/√2
f0 = frekvens[idx_f0]
print(f"Estimert grensefrekvens (f0): {f0} Hz")

# Beregn teoretiske verdier
H_teoretisk = 1 / np.sqrt(1 + (frekvens / f0) ** 2)
fase_teoretisk = np.arctan(frekvens / f0) * (180 / np.pi)  # Endret til +arctan

# Opprett en figur med tre subplots (1x3)
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Amplitudekarakteristikk (semilog x-akse, lineær y-akse med Vut/Vinn)
axes[0].semilogx(frekvens, forsterkning, marker='o', color="g", linestyle='-', label="Målt")
axes[0].semilogx(frekvens, H_teoretisk, linestyle='--', color="r", label="Teoretisk")
axes[0].axvline(f0, color='b', linestyle=':', label=f"f0 = {f0:.1f} Hz")
axes[0].set_xlabel("Frekvens (Hz)")
axes[0].set_ylabel("Forsterkning (Vut/Vinn)")
axes[0].set_title("Amplitudekarakteristikk")
axes[0].grid(True, which="both", linestyle="--", linewidth=0.5)
axes[0].legend()

# Fasekarakteristikk (semilog x-akse, lineær y-akse)
axes[1].semilogx(frekvens, faseforskjell, marker='o', linestyle='-', label="Målt")
axes[1].semilogx(frekvens, fase_teoretisk, linestyle='--', color="r", label="Teoretisk")
axes[1].set_xlabel("Frekvens (Hz)")
axes[1].set_ylabel("Faseforskjell (grader)")
axes[1].set_title("Fasekarakteristikk")
axes[1].grid(True, which="both", linestyle="--", linewidth=0.5)
axes[1].legend()

# Juster layout og vis figuren
plt.tight_layout()
plt.show()


# Figur 2: Forskjell mellom teoretisk og målt
fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5))

# Forsterkning (prosentvis forskjell)
forskjell_forsterkning = (forsterkning - H_teoretisk)  # Forskjell i prosent
axes2[0].semilogx(frekvens, forskjell_forsterkning, marker='o', color="purple", linestyle='-', label="Forskjell (Forsterkning)")
axes2[0].set_xlabel("Frekvens (Hz)")
axes2[0].set_ylabel("Forskjell")
axes2[0].set_title("Forskjell i Forsterkning mellom teoretisk og målt")
axes2[0].grid(True, which="both", linestyle="--", linewidth=0.5)
axes2[0].legend()

# Faseforskjell (forskjell i grader)
forskjell_fase = faseforskjell - fase_teoretisk  # Forskjell i grader
axes2[1].semilogx(frekvens, forskjell_fase, marker='o', color="orange", linestyle='-', label="Forskjell (Fase i grader)")
axes2[1].set_xlabel("Frekvens (Hz)")
axes2[1].set_ylabel("Forskjell (grader)")
axes2[1].set_title("Forskjell i Fase mellom teoretisk og målt")
axes2[1].grid(True, which="both", linestyle="--", linewidth=0.5)
axes2[1].legend()

# Juster layout og vis den andre figuren
plt.tight_layout()
plt.show()
