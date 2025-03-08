import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def prep(n):
    data = pd.read_excel(f"Run {n}.xlsx", header=None).to_numpy()[1:]
    temperatur = data[:, 0]
    spenning = data[:, 1]
    return temperatur, spenning

temp1, spenning1 = prep(1)
temp2, spenning2 = prep(2)

figur1, akser1 = plt.subplots(1, 2, figsize=(12, 5))

# Forsøk 1
akser1[0].scatter(temp1, spenning1, color="blue", label="Måledata")
akser1[0].set_title("Datapunkter - Forsøk 1")
akser1[0].set_xlabel("Temperatur (°C)")
akser1[0].set_ylabel("Spenning (mV)")
akser1[0].legend()
akser1[0].grid()

# Forsøk 2
akser1[1].scatter(temp2, spenning2, color="green", label="Måledata")
akser1[1].set_title("Datapunkter - Forsøk 2")
akser1[1].set_xlabel("Temperatur (°C)")
akser1[1].set_ylabel("Spenning (mV)")
akser1[1].legend()
akser1[1].grid()

plt.tight_layout()
plt.show()