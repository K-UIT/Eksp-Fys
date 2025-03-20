import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyvisa
import time

# Kobler seg til Oscillioskopet
rm = pyvisa.ResourceManager()
resources = rm.list_resources()
osc = rm.open_resource(resources[0])

# Default setup av oscilloscope
osc.write(r':SYSTem:PRESet')
osc.write(r':CHANnel2:DISPlay on')
osc.write(r':CHANnel2:PROBe 1')

# Starter wave generator med 5V sinus
osc.write(r'WGEN:OUTPut on')
osc.write(r"WGEN:FUNCtion SINusoid")
osc.write(r"WGEN:VOLTage 5")

# lager lister for frekvens, volt ved kanal 1, volt ved kanal 2 og fase
F = []
V_inn = []
V_ut = []
phase = []

# Lager en logaritmisk frekvens "sweep"
a1 = 10.**(np.arange(3, 6))
a2 = np.arange(1, 10, 0.1)
logrange = np.outer(a1, a2).flatten()[:-89]
print(logrange)
print(len(logrange))

#Går gjennom alle frekvensene
for i in logrange:
    osc.write(f':WGEN:FREQuency {i}Hz')  # Setter frekvens
    osc.write(':AUTOSCALE channel1,channel2')  # Autoscale channel 1 og 2
    time.sleep(0.5)  # Venter for å få stabil avlesning

    # Måler spenning
    V_inn.append(float(osc.query(':MEASure:VPP? CHANnel1')))
    V_ut.append(float(osc.query(':MEASure:VPP? CHANnel2')))

    # Måler fase
    phase.append(float(osc.query(':MEASure:PHASe? CHANnel1,CHANnel2')))

    # Lagrer frekvens
    F.append(i)

# Lagrer alt som en dataframe
df = pd.DataFrame({'F': F, 'V_inn': V_inn, 'V_ut': V_ut, 'phase': phase})
df = df.replace('E', 'e', regex=True).replace(',', '.', regex=True)
df = df.apply(pd.to_numeric, errors='coerce')

# Lagrer en kollonne med dB verdiene
df['dB'] = 20 * np.log10(df["V_ut"] / df["V_inn"])

# Printer ut dataframen
print(df)
# Lagrer alt i en csv fil
df.to_csv(str(input("Filnavn: ")+".csv"))

# Plotter for sjekk
fig, axes = plt.subplots(2, 1)

axes[0].plot(df["F"], df["dB"])
axes[0].set_xscale("log")
axes[0].set_xlabel('Frekvens [Hz]', fontsize=12)
axes[0].set_ylabel('20log(H(f)) [dB]', fontsize=12)
axes[0].tick_params(axis='x', labelsize=12)
axes[0].tick_params(axis='y', labelsize=12)

axes[1].plot(df["F"], df['phase'])
axes[1].set_xscale("log")
axes[1].set_xlabel('Frekvens [Hz]', fontsize=12)
axes[1].set_ylabel('Fase [grader]', fontsize=12)
axes[1].tick_params(axis='x', labelsize=12)
axes[1].tick_params(axis='y', labelsize=12)

plt.show()
