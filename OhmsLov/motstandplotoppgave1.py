import matplotlib.pyplot as plt


plt.figure(figsize=(6, 3))
plt.errorbar(0, 1179, 1179*0.5/100, fmt='o', color='r', capsize=10, capthick=1.5, elinewidth=1.5, label="Målt")
plt.errorbar(1, 1179.71111, 0.00022, fmt='o', color='b', capsize=10, capthick=1.5, elinewidth=1.5, label="Lineær regresjon 1V")
plt.errorbar(2, 1179.27493, 0.00235, fmt='o', color='g', capsize=10, capthick=1.5, elinewidth=1.5, label="Lineær regresjon 10V")
plt.xticks([0,1,2], ["Målt verdi", "1V","10V"], fontsize=12)
plt.ylabel("Motstand R(Ω)", fontsize=12)
plt.xlabel("Resultater", fontsize=12)
plt.title("Sammenligning av resistans verdier", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tick_params(axis="both", labelsize=8)
plt.show()