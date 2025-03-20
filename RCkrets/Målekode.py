import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyvisa
import time

# Print available resources connected to the computer
rm = pyvisa.ResourceManager()
resources = rm.list_resources()

# Open the oscilloskope
osc = rm.open_resource(resources[0])

# Default setup of oscilloscope
osc.write(r':SYSTem:PRESet')
osc.write(r':CHANnel2:DISPlay on')
osc.write(r':CHANnel2:PROBe 1')

# Start wave generator on oscilloscope: 5V sinus
osc.write(r'WGEN:OUTPut on')
osc.write(r"WGEN:FUNCtion SINusoid")
osc.write(r"WGEN:VOLTage 5")

# Create arrays for frequency, voltage at channel 1, voltage at channel 2, and phase
F = []
V_inn = []
V_ut = []
phase = []

# Create logarithmic range for frequency sweep
a1 = 10.**(np.arange(3, 6))
a2 = np.arange(1, 10, 0.1)
logrange = np.outer(a1, a2).flatten()[:-89]
print(logrange)
print(len(logrange))

# Sweep all frequencies and measure voltage in, voltage out, and phase
for i in logrange:
    osc.write(f':WGEN:FREQuency {i}Hz')  # Set frequency
    osc.write(':AUTOSCALE channel1,channel2')  # Autoscale channel 1
    #osc.write(':AUTOSCALE channel2')  # Autoscale channel 2
    time.sleep(0.5)  # Allow time for stabilization

    # Measure voltages
    V_inn.append(float(osc.query(':MEASure:VPP? CHANnel1')))
    V_ut.append(float(osc.query(':MEASure:VPP? CHANnel2')))

    # Measure phase
    phase.append(float(osc.query(':MEASure:PHASe? CHANnel1,CHANnel2')))

    # Store frequency
    F.append(i)

# Save frequency and voltages as pandas dataframe
df = pd.DataFrame({'F': F, 'V_inn': V_inn, 'V_ut': V_ut, 'phase': phase})
df = df.replace('E', 'e', regex=True).replace(',', '.', regex=True)
df = df.apply(pd.to_numeric, errors='coerce')

# Create column with the transfer function in dB
df['dB'] = 20 * np.log10(df["V_ut"] / df["V_inn"])

# Print the pandas dataframe for a visual check
print(df)
# Save the pandas dataframe as a CSV file
df.to_csv(str(input("Filnavn: ")+".csv"))

# Plot amplitude (in dB) and phase against frequency
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