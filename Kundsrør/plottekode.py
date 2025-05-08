import numpy as np
import matplotlib.pyplot as plt

# Konstanter
R = 8.3144
T = 25 + 273.15  # Kelvin

# Måleserier og metadata
data = {
    "Luft": [
        {"a1": [55.6, 55.8, 55.8, 56, 55.7], "a2": [24, 23.9, 23.8, 23.9, 23.9], "n": 0, "f": 546},
        {"a1": [66.5, 66.5, 66.7, 66.6, 66.7], "a2": [15.9, 15.3, 15.5, 15.6, 15.4], "n": 1, "f": 669},
        {"a1": [80.2, 80, 80.5, 80.3, 80.4], "a2": [11.2, 11.1, 11.3, 11, 11.1], "n": 2, "f": 750},
    ],
    "Argon": [
        {"a1": [68.9, 69.4, 69.5, 68.4, 69.1], "a2": [17, 16.3, 16.2, 15.9, 16.1], "n": 1, "f": 608},
        {"a1": [71.2, 71.4, 72.7, 72.4, 72.3], "a2": [8.6, 7.7, 7.6, 7, 7.5], "n": 2, "f": 760},
        {"a1": [73.1, 73.7, 73.8, 73.6, 73.7], "a2": [5.7, 5.2, 5.3, 5.2, 5.4], "n": 5, "f": 1410},
    ]
}

molmasser = {"Luft": 28.8 / 1000, "Argon": 40 / 1000}  # kg/mol

# Funksjon for å beregne verdier og usikkerheter
def calc(a1, a2, n, f, M):
    mean1, mean2 = np.mean(a1), np.mean(a2)
    std1, std2 = np.std(a1, ddof=1), np.std(a2, ddof=1)
    delta_L = (mean1 - mean2) / 100
    delta_L_unc = (std1 + std2) / 100

    lam = 2 * delta_L / (n + 1)

    v = lam * f
    v_unc = v * (delta_L_unc / delta_L + 0.5 / f)

    gamma = (v**2 * M) / (R * T)
    gamma_unc = gamma * (2 * 0.5/f + 2 * (delta_L_unc / delta_L) + 0.2/25)

    frihetsgrader = 2 / (gamma - 1)
    frihetsgrader_unc = frihetsgrader * (gamma_unc/ (gamma - 1))
    print(f"{f} Hz: {round(gamma, 2)} ± {round(gamma_unc, 2)}")
    print("-"*40)
    return v, v_unc, frihetsgrader, frihetsgrader_unc, gamma, gamma_unc

# Kalkuler resultater for alle forsøk
results = {"Luft": [], "Argon": []}

for gass, målinger in data.items():
    for m in målinger:
        res = calc(m["a1"], m["a2"], m["n"], m["f"], molmasser[gass])
        results[gass].append(res)

# Vektet middelverdi
def weighted_average(values, uncertainties):
    weights = 1 / np.array(uncertainties) ** 2
    avg = np.sum(weights * values) / np.sum(weights)
    unc = 1 / np.sqrt(np.sum(weights))
    return avg, unc

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # 2x2 ruter
fig.suptitle('Måleresultater for Luft og Argon', fontsize=18)

gasser = ["Luft", "Argon"]
parametre = ["Bølgehastighet", "Frihetsgrader"]
print("\nVektet snitt for adiabatkonstant (gamma):")
for gass in gasser:
    gammas = [r[4] for r in results[gass]]        # gamma ligger på indeks 4
    gamma_uncs = [r[5] for r in results[gass]]     # gamma_unc ligger på indeks 5
    avg_gamma, unc_gamma = weighted_average(np.array(gammas), np.array(gamma_uncs))
    print(f"{gass}: {avg_gamma:.3f} ± {unc_gamma:.3f}")
for idx, gass in enumerate(gasser):
    for i, key in enumerate(parametre):
        ax = axs[idx, i]
        values = [r[i*2] for r in results[gass]]
        uncs = [r[i*2+1] for r in results[gass]]
        avg, avg_unc = weighted_average(np.array(values), np.array(uncs))
        ax.errorbar(0, avg, yerr=avg_unc, fmt='o', color='red', capsize=5, label=f'Vektet snitt: {round(avg,2)}±{round(avg_unc,2)}')
        ax.errorbar(range(1, 4), values, yerr=uncs, fmt='o', linestyle='None', color='blue', capsize=5, label='Enkeltmålinger')
        ax.set_xticks(range(4))
        ax.set_ylabel(key, fontsize=12)
        ax.set_xlabel("Målesett", fontsize=12)
        ax.set_title(f"{gass} - {key}", fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(axis='y', linestyle='-', alpha=0.5)

        if gass == "Argon":
            ax.set_xticklabels(["Snitt", "608 Hz", "760 Hz", "1410 Hz"], fontsize=11)
            if i == 0:
                ax.axhline(y=308 + 0.56*(25-0.2), color='green', linestyle="--", label=f"Forventet bølgefart: {308 + 0.56*25:.1f}±{0.2*0.56:.1f} m/s")
                ax.axhline(y=308 + 0.56*(25+0.2), color='green', linestyle="--")
            else:
                ax.axhline(y=3, color='orange', linestyle="--", label="Forventet frihetsgrader: 3")
        elif gass == "Luft":
            ax.set_xticklabels(["Snitt", "546 Hz", "669 Hz", "750 Hz"], fontsize=11)
            if i == 0:
                ax.axhline(y=331.45 + 0.59*(25-0.2), color='green', linestyle="--", label=f"Forventet bølgefart: {331.45 + 0.59*25:.1f}±{0.2*0.59:.1f} m/s")
                ax.axhline(y=331.45 + 0.59*(25+0.2), color='green', linestyle="--")
            else:
                ax.axhline(y=5, color='orange', linestyle="--", label="Forventet frihetsgrader: 5")

        ax.legend(fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
