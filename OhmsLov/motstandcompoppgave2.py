import matplotlib.pyplot as plt

# Oppsett navn
oppsett = ["Målt", "Kobling A", "Kobling B", "Kobling C", "Kobling D"]
x_val = range(len(oppsett))

# Farger for hver kobling
farger = ["k", "r", "b", "g", "m"]

# Målt motstand og usikkerhet
malt_motstand = [9.76, 1499, 4.70e6]
malt_usikker = [0.05, 8, 0.02e6]

# Målt motstand og usikkerhet fra tabellene
motstander = [
    [12.0, 1500, 4.60e6],  # Kobling A
    [9.5, 1510, 4.71e6],   # Kobling B
    [9.96, 1510, 3.17e6],  # Kobling C
    [12.79, 1520, 4.62e6]  # Kobling D
]

usikkerhet = [
    [1.1, 20, 0.06e6],  # Kobling A
    [0.9, 30, 0.07e6],  # Kobling B
    [0.14, 20, 0.04e6], # Kobling C
    [0.15, 20, 0.06e6]  # Kobling D
]

# Figur med 3 subplots (måling 1, 2 og 3)
fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)

for i in range(3):  # Måling 1, 2, 3
    # Samle data for hver måling
    maling = [malt_motstand[i]] + [motstander[j][i] for j in range(4)]
    rel_usikkerhet = [malt_usikker[i]] + [usikkerhet[j][i] for j in range(4)]

    # Plot error bars
    for j in range(5):  # 1 målt verdi + 4 koblinger
        axes[i].errorbar(x_val[j], maling[j], yerr=rel_usikkerhet[j], fmt="o",
                         color=farger[j], capsize=6, capthick=1.5, elinewidth=1.5,
                         label=oppsett[j] if i == 0 else "")

    axes[i].set_ylabel("Motstand R (Ω)", fontsize=12)
    axes[i].set_title(f"Måling {i+1}", fontsize=14)
    axes[i].grid(True, linestyle="--", alpha=0.7)
    axes[i].tick_params(axis="both", labelsize=10)

axes[-1].set_xticks(x_val)
axes[-1].set_xticklabels(oppsett, fontsize=12)
axes[0].legend(fontsize=10, loc="lower right")

plt.suptitle("Sammenligning av motstandsverdier for hver måling", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
