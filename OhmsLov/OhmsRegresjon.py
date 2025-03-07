import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

def analyser_ohms_lov(nummer):
    # Forbereder data
    data = pd.read_excel(f"OhmsLov{nummer}V.xlsx", header=None).to_numpy()[1:17]
    n = data.shape[0]
    spenning = data[:, 1]
    strom = data[:, 2]
    err_spenning = data[:, 3]
    err_strom = data[:, 4]
    sx = np.sum(strom)
    sx2 = np.sum(strom**2)
    sy = np.sum(spenning)
    sxy = np.sum(strom * spenning)
    
    # Regner ut A og B
    A = (n * sxy - sx * sy) / (n * sx2 - sx**2)
    B = (sy - A * sx) / n
    
    # Regner ut den lineære approksimasjonen
    spenning_hat = A * strom + B
    SSE_lin = np.sum((spenning - spenning_hat) ** 2)
    
    # Usikkerhet i utregningene
    sigma_y = sqrt(SSE_lin / (n - 2))
    sigma_A = sigma_y * sqrt(sx2 / (n * sx2 - sx**2))
    sigma_B = sigma_y * sqrt(n / (n * sx2 - sx**2))
    
    # Printer ut verdier
    print(f"Lineær tilpasning for {nummer}V:")
    print(f"Resistans (A) = {A:.5f} Ω, Konstantledd (B) = {B:.5f} V")
    print(f"SSE (lineær): {SSE_lin:.8f}")
    print(f"Usikkerhet: sigma_A = {sigma_A:.5f}, sigma_B = {sigma_B:.5f}")
    print("-" * 40)
    
    return strom * 1e3, spenning, spenning_hat, A, B, err_spenning, err_strom * 1e3

strom_1V, spenning_1V, spenning_hat_1V, A_1V, B_1V, err_spenning1V, err_strom1V = analyser_ohms_lov(1)
strom_10V, spenning_10V, spenning_hat_10V, A_10V, B_10V, err_spenning10V, err_strom10V = analyser_ohms_lov(10)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot 1V
axes[0].errorbar(strom_1V, spenning_1V, xerr=err_strom1V, yerr=err_spenning1V, fmt="o", color="blue", label="Måledata 1V", ecolor='purple', capsize=5, elinewidth=2)
axes[0].plot(strom_1V, spenning_hat_1V, color="red", label=f"Lineær: V = {A_1V:.2f}I {B_1V:+.2f}")
axes[0].set_xscale("log")
axes[0].set_yscale("log")
axes[0].set_xlabel("Strøm (mA)", fontsize=14)
axes[0].set_ylabel("Spenning (V)", fontsize=14)
axes[0].set_title("Ohms lov - 1V", fontsize=16)
axes[0].legend(fontsize=12)
axes[0].grid(True, which="both", linestyle="--", linewidth=0.5)

# Plot 10V
axes[1].errorbar(strom_10V, spenning_10V, xerr=err_strom10V, yerr=err_spenning10V, fmt="o", color="green", label="Måledata 10V", ecolor='purple',capsize=5, elinewidth=2)
axes[1].plot(strom_10V, spenning_hat_10V, color="red", label=f"Lineær: V = {A_10V:.2f}I {B_10V:+.2f}")
axes[1].set_xscale("log")
axes[1].set_yscale("log")
axes[1].set_xlabel("Strøm (mA)", fontsize=14)
axes[1].set_title("Ohms lov - 10V", fontsize=16)
axes[1].legend(fontsize=12)
axes[1].grid(True, which="both", linestyle="--", linewidth=0.5)

plt.tight_layout()
plt.show()

# Beregning av residualer
residuals_1V = spenning_1V - spenning_hat_1V
residuals_10V = spenning_10V - spenning_hat_10V

fig, axes = plt.subplots(2, 1, figsize=(8, 6))

# Residualer for 1V
axes[0].errorbar(strom_1V, residuals_1V, xerr=err_strom1V, yerr=err_spenning1V, fmt="o", color="blue", label="Residualer 1V", ecolor='purple',capsize=5, elinewidth=2)
axes[0].axhline(0, color="black", linestyle="--")
axes[0].set_xscale("log")
axes[0].set_xlabel("Strøm (mA)")
axes[0].set_ylabel("Residual (V)")
axes[0].set_title("Residualer - 1V")
axes[0].legend()
axes[0].grid(True, which="both", linestyle="--", linewidth=0.5)
axes[0].tick_params(axis='both', labelsize=12)  

# Residualer for 10V
axes[1].errorbar(strom_10V, residuals_10V, xerr=err_strom10V, yerr=err_spenning10V, fmt="o", color="green", label="Residualer 10V", ecolor='purple',capsize=5, elinewidth=2)
axes[1].axhline(0, color="black", linestyle="--")
axes[1].set_xscale("log")
axes[1].set_xlabel("Strøm (mA)")
axes[1].set_ylabel("Residual (V)")
axes[1].set_title("Residualer - 10V")
axes[1].legend()
axes[1].grid(True, which="both", linestyle="--", linewidth=0.5)
axes[1].tick_params(axis='both', labelsize=12)  

plt.tight_layout()
plt.show()
