import pandas as pd
import matplotlib.pyplot as plt

def data_plot(nummer, start, fase_tid, farge, navn):
    # Leser excel-filen
    data = pd.read_excel(f"nitrogen {nummer}.xlsx", header=None)
    data = data.to_numpy()
    data = data[1:]

    # Temperatur og tid som arrays
    Temp = data[start-200:, 0]
    Tid = data[start-200:, 1]

    plt.figure(figsize=(8, 5))

    # Tegner inn før temperaturøkning
    før = Tid < start
    plt.scatter(Tid[før], Temp[før], color=farge[0], label=navn[0])

    # Tegner inn de andre fasene
    for i, (fase_start, fase_end) in enumerate(fase_tid):
        fase = (Tid > fase_start) & (Tid <= fase_end)
        plt.scatter(Tid[fase], Temp[fase], color=farge[i+1], label=navn[i+1])

    plt.ylabel("Temperatur (°C)")
    plt.xlabel("Tid (s)")
    plt.legend()
    plt.grid()
    plt.title(f"Forsøk {nummer}")
    plt.show()

# Fasene for hver av forsøkene
faser_1 = [(1033, 1301), (1301, 1950), (1950, 2330)]
faser_2 = [(720, 848), (848, 1545), (1545, 2000)]
faser_3 = [(620, 781), (781, 1377), (1377, 1670)]

# Definerer farger for hver fase
fase_farge= ["gray", "red", "green", "blue"]

# Definerer navn for hver fase
fase_navn = ["Før temperaturøkning", "Oppvarming", "Hvileperiode", "Nedkjøling"]

# Plotter de tre forsøkene med faser
data_plot("1", 1033, faser_1, fase_farge, fase_navn)
data_plot("2", 720, faser_2, fase_farge, fase_navn)
data_plot("3", 620, faser_3, fase_farge, fase_navn)
