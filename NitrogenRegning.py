import matplotlib.pyplot as plt

def finn_TN(P, dPp, t, dt, m, dm, c, dc, temp_før_oppvarming, temp_etter_oppvarming, dDT1, temp_før_lodd, temp_etter_likevekt, dDT2, dT2):
    # før regning
    dP = P*dPp
    c = c/1000
    Ts = temp_etter_likevekt
    
    # Temperaturendringer
    DT1 = temp_etter_oppvarming - temp_før_oppvarming
    DT2 = temp_før_lodd - temp_etter_likevekt
    # Beregning av varmekapasitet for kalorimeteret
    C0 = P * t / DT1
    k = C0 / (m * c)

    # Usikkerhetsberegninger
    dC0 = C0 * (dP/P + dt/t + dDT1/DT1)
    dK = k * (dC0/C0 + dm/m + dc/c)
    dTN = dT2 + k * dDT2 + DT2 * dK
    
    # Beregning av TN
    TN = Ts - k * DT2
    
    print("Temperatur på nitrogen: ", TN)
    print("Usikkerhet: ", dTN)
    print(f"Prediksjonsintervall:\n({round(TN-dTN,4)},{round(TN+dTN,4)},)\n\n")
    return TN, dTN


# Forsøk 1
print("Forsøk 1:")
f1_TN, f1_dTN = finn_TN(317.7, 0.005, 1301-1033, 2, 994.84, 0.01, 129, 0, 10.27, 29.53, 0.5*2, 28.52, 21.96, 0.5*2, 0.5)

# Forsøk 2
print("Forsøk 2:")
f2_TN, f2_dTN = finn_TN(317.3, 0.005, 848-720, 2, 994.84, 0.01, 129, 0, 13.31, 25.16, 0.5*2, 25.33, 17.14, 0.5*2, 0.5)

# Forsøk 3
print("Forsøk 3:")
f3_TN, f3_dTN = finn_TN(316.7, 0.005, 781-620, 2, 994.84, 0.01, 129, 0, 11.73, 25.09, 0.5*2, 25.32, 18.13, 0.5*2, 0.5)

# Plotter
TN = -202.8975
dTN = 7.1025
y = [TN, f1_TN, f2_TN, f3_TN]
y_error = [dTN, f1_dTN, f2_dTN, f3_dTN]
x = [0, 1, 2, 3]

# Plot
plt.figure(figsize=(6, 4))

# Plotter "sann verdi" i rød
plt.errorbar(x[0], y[0], yerr=y_error[0], fmt='o', color='r', capsize=10, capthick=1.5, elinewidth=1.5, label="Tabell verdi")

# Plotter forsøkene i blått
plt.errorbar(x[1:], y[1:], yerr=y_error[1:], fmt='o', color='b', capsize=10, capthick=1.5, elinewidth=1.5, label="Forsøk")

# Aksetitler og grid
plt.xticks(x, ["Forventet verdi", "Forsøk 1", "Forsøk 2", "Forsøk 3"])
plt.ylabel("Temperatur (°C)")
plt.xlabel("Måling")
plt.title("Målinger av flytende nitrogen temperatur")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.show()
