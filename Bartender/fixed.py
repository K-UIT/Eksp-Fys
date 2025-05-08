import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
g = 9.81  # tyngdeakselerasjon

def behandle_excel_run(filepath):
    # Lager en padas dataframe
    df = pd.read_excel(filepath)
    gjennomsnittlige_mu = [] # Alle gjennomsnittlige mu
    alle_mu = []
    num_runs = df.shape[1] // 3  # en run er 3 kolonner

    for i in range(num_runs):
        t_col = df.columns[i*3] # Tid er 1
        x_col = df.columns[i*3 + 1] # Posisjon er 2
        v_col = df.columns[i*3 + 2] # Hastighet er 3

        run_df = df[[t_col, x_col, v_col]].copy()
        run_df.columns = ['t', 'x', 'v'] # Navngir kolonner

        # Finn maks fart
        v_max_index = run_df['v'].abs().idxmax()

        # Ta ut snittdata etter maks fart og til nær stopp
        subset = run_df.iloc[v_max_index:].reset_index(drop=True)
        subset = subset[subset['v'] < -0.01].reset_index(drop=True)

        mu_vals = []
        for j in range(len(subset) - 1):
            v1 = subset.loc[j, 'v']
            v2 = subset.loc[j + 1, 'v']
            x1 = subset.loc[j, 'x']
            x2 = subset.loc[j + 1, 'x']
            l = x2 - x1
            if l != 0:
                mu = (v2**2 - v1**2) / (2*g*l)
                mu_vals.append(mu)
                alle_mu.append(mu)
        if len(mu_vals) > 1:
            mu_mean = sum(mu_vals[1:]) / len(mu_vals[1:])  # mu per run
            gjennomsnittlige_mu.append(mu_mean)
        else:
            gjennomsnittlige_mu.append(None)  # tom run


    # Konverter til DataFrame
    mu_df = pd.DataFrame({'Run': list(range(1, num_runs + 1)), 'mu': gjennomsnittlige_mu})

    all_avg_mu = pd.DataFrame({"amu": alle_mu})["amu"].dropna()

    return all_avg_mu, all_avg_mu.mean(), all_avg_mu.std(ddof=1)




R1, _, _=behandle_excel_run('Måledata 0L.xlsx')
R2,mean_R2,std_R2=behandle_excel_run('Måledata 0,25L.xlsx')
R3,mean_R3,std_R3=behandle_excel_run('Måledata 0,55L.xlsx')

def beregn_vektet_gjennomsnitt(filbaner):
    # Liste for resultater
    resultater = []

    # Behandle hver fil
    for filepath in filbaner:
        mu, mean_mu, std_mu = behandle_excel_run(filepath)
        resultater.append((mean_mu, std_mu))
        print(f"{filepath}: mean = {mean_mu:.5f}, std = {std_mu:.5f}")

    # Beregn vekter og vektet gjennomsnitt
    vekter = [1 / std**2 for _, std in resultater]
    vektet_mean = sum(vekter[i] * resultater[i][0] for i in range(len(resultater))) / sum(vekter)
    vektet_std = np.sqrt(1 / sum(vekter))

    print(f"\nVektet gjennomsnitt: {vektet_mean:.5f}")
    print(f"Vektet standardavvik: {vektet_std:.5f}")
    
    return vektet_mean, vektet_std

# Filbaner
filepaths = ['Måledata 0L.xlsx', 'Måledata 0,25L.xlsx', 'Måledata 0,55L.xlsx']

# Kjør funksjonen
weighted_mean, weighted_std = beregn_vektet_gjennomsnitt(filepaths)




plt.figure(figsize=(7, 3))
plt.hist([R1, R2, R3], bins=200, stacked=True, label=['0L', '0,25L', '0,55L'],
         color=['skyblue', 'lightgreen', 'salmon'], edgecolor='black')

# Legg til linjer
plt.axvline(weighted_mean, color='black', linestyle='-', linewidth=2, label=f'Vektet gjennomsnitt: {round(weighted_mean,2)}')
plt.axvline(weighted_mean + weighted_std, color='black', linestyle='--', linewidth=1.5, label=f'Standardavvik: {round(weighted_std,2)}')
plt.axvline(weighted_mean - weighted_std, color='black', linestyle='--', linewidth=1.5)

# Tittel og akser
plt.title('Fordeling av friksjonskoeffisient μ per Run – stacked')
plt.xlabel('μ-verdi')
plt.ylabel('Antall')
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.show()


def evaluer_forventet_vs_målt(mu, mu_std, filepaths):
    resultater = []
    for filepath in filepaths:
        df = pd.read_excel(filepath)
        num_runs = df.shape[1] // 3  # hver run består av 3 kolonner

        for i in range(num_runs):
            try:
                t_col = df.columns[i*3]
                x_col = df.columns[i*3 + 1]
                v_col = df.columns[i*3 + 2]

                run_df = df[[t_col, x_col, v_col]].copy()
                run_df.columns = ['t', 'x', 'v']

                # Finne maks fart
                v_max_index = run_df['v'].abs().idxmax()
                
                # Startverdier
                start_x = run_df.loc[v_max_index, 'x']

                # Bruk data etter v_max
                subset = run_df.iloc[v_max_index:].reset_index(drop=True)
                subset = subset[subset['v'] < -0.01].reset_index(drop=True)

                if subset.shape[0] < 2:
                    print(f"Ikke nok data i run {i+1} i fil {filepath}")
                    continue

                # Faktisk målt forflytning
                slutt_x = subset.iloc[-1]['x']
                faktisk_l = abs(slutt_x - start_x)

                # Estimert forventet lengde ved å summere over små intervaller
                forventet_l = 0
                for j in range(len(subset) - 1):
                    v1 = subset.loc[j, 'v']
                    v2 = subset.loc[j + 1, 'v']
                    delta_v2 = v2**2 - v1**2
                    dx = delta_v2 / (2 * g * mu)
                    forventet_l += abs(dx)  # Tar absoluttverdien for sikkerhet

                # Usikkerheten på summert lengde
                forventet_l_std = forventet_l * (mu_std / mu+2*0.001/(abs(subset['v'].abs().max())))

                # Lagre resultat
                resultater.append({
                    'Fil': filepath,
                    'Run': i + 1,
                    'Faktisk lengde (m)': faktisk_l,
                    'Forventet lengde (m)': forventet_l,
                    'Usikkerhet (m)': forventet_l_std,
                    'Avvik (m)': faktisk_l - forventet_l
                })

            except Exception as e:
                print(f"Feil i run #{i+1} i fil {filepath}: {e}")

    resultater_df = pd.DataFrame(resultater)
    return resultater_df



# Sett inn filbanene
filepaths = ['Måledata 0L.xlsx', 'Måledata 0,25L.xlsx', 'Måledata 0,55L.xlsx']

# Bruker vektet mean og std vi fant tidligere
resultater = evaluer_forventet_vs_målt(weighted_mean, weighted_std, filepaths)

# Viser resultatene
print(resultater)

def plot_avvik_med_usikkerhet(resultater_df):
    import matplotlib.pyplot as plt

    # Kopier og sorter etter faktisk lengde
    df = resultater_df.copy()
    df = df.sort_values(by='Faktisk lengde (m)', ascending=True).reset_index(drop=True)

    # Rens filnavn og legg til ny kolonne
    df['Label'] = df['Fil'].str.replace('.xlsx', '', regex=False)

    # Farger per renset navn
    fargekart = {
        'Måledata 0L': 'skyblue',
        'Måledata 0,25L': 'lightgreen',
        'Måledata 0,55L': 'salmon'
    }

    plt.figure(figsize=(9, 3))

    for i, row in df.iterrows():
        farge = fargekart.get(row['Label'], 'gray')
        plt.errorbar(i + 1, row['Avvik (m)'], yerr=row['Usikkerhet (m)'],
                     fmt='o', color=farge, ecolor='black', elinewidth=1.5, capsize=4)

    # Referanselinje
    plt.axhline(0, color='blue', linestyle='--', linewidth=2, label='Forventet (0-avvik)')

    # Forklaring (legend)
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                                  markerfacecolor=color, markersize=10)
                       for label, color in fargekart.items()]
    legend_elements.append(plt.Line2D([0], [0], linestyle='--', color='blue', label='0-Avvik'))

    plt.legend(handles=legend_elements)
    plt.title('Avvik mellom målt og forventet distanse\nSortert etter faktisk distanse')
    plt.xlabel('Run (sortert etter faktisk lengde, lavest til høyest)')
    plt.ylabel('Avvik (målt - forventet) [m]')
    plt.grid(True)
    plt.tight_layout()
    plt.show()



plot_avvik_med_usikkerhet(resultater)

def vektet_middel_med_usikkerhet(avvik, usikkerhet):
    # Beregn vektene
    vekter = 1 / (usikkerhet ** 2)
    
    # Vektet gjennomsnitt
    vektet_middel = (vekter * avvik).sum() / vekter.sum()
    
    # Felles usikkerhet
    samlet_usikkerhet = (1 / vekter.sum())**0.5
    
    return vektet_middel, samlet_usikkerhet

# Bruk på dine data:
avvik = resultater['Avvik (m)']
usikkerhet = resultater['Usikkerhet (m)']

vektet_avvik, samlet_usikkerhet = vektet_middel_med_usikkerhet(avvik, usikkerhet)

print(f"\nVektet gjennomsnittlig avvik: {vektet_avvik*100:.2f} cm")
print(f"Samlet usikkerhet: ±{samlet_usikkerhet*100:.2f} cm")

# Beregn hvor mange datapunkter som er innenfor ±1 std.avvik
alle_mu = pd.concat([R1, R2, R3])
total = len(alle_mu)
innenfor_std = alle_mu[(alle_mu > (weighted_mean - weighted_std)) & (alle_mu < (weighted_mean + weighted_std))]
prosent_innenfor = len(innenfor_std) / total * 100

print(f"Andel av datapunkter innenfor ±1 standardavvik: {prosent_innenfor:.2f}%")


def plot_faktisk_vs_forventet(resultater_df):

    df = resultater_df.copy()
    
    # Farger per filnavn
    df['Label'] = df['Fil'].str.replace('.xlsx', '', regex=False)
    fargekart = {
        'Måledata 0L': 'skyblue',
        'Måledata 0,25L': 'lightgreen',
        'Måledata 0,55L': 'salmon'
    }

    plt.figure(figsize=(7, 3))

    for label, gruppe in df.groupby('Label'):
        farge = fargekart.get(label, 'gray')
        plt.errorbar(
            gruppe['Faktisk lengde (m)'], gruppe['Forventet lengde (m)'],
            xerr=0.001, yerr=gruppe['Usikkerhet (m)']+(3.23+0.67)/100,
            fmt='o', label=label, color=farge, ecolor='black',
            elinewidth=1, capsize=3
        )

    # Diagonal linje for y = x
    min_lengde = min(df['Faktisk lengde (m)'].min(), df['Forventet lengde (m)'].min())
    max_lengde = max(df['Faktisk lengde (m)'].max(), df['Forventet lengde (m)'].max())
    plt.plot([min_lengde, max_lengde], [min_lengde, max_lengde], 'k--', linewidth=2, label='y = x')

    plt.xlabel('Faktisk målt lengde [m]')
    plt.ylabel('Forventet (beregnet) lengde [m]')
    plt.title('Faktisk vs. forventet lengde med usikkerhet')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


plot_faktisk_vs_forventet(resultater)

# Kombiner alle datasettene for samlet visning
alle_mu = pd.concat([R1, R2, R3])

# Lag boxplot
data = [alle_mu, R1, R2, R3]
labels = ['Samlet', '0L', '0,25L', '0,55L']

plt.figure(figsize=(6, 3))
bp = plt.boxplot(
    data,
    labels=labels,
    patch_artist=True,
    medianprops=dict(color='red'),
    flierprops=dict(marker='o', markerfacecolor='gray', markersize=6, linestyle='none')
)

# Sett farge per boks
colors = ['lightcoral', 'lightblue', 'lightblue', 'lightblue']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

plt.title('Boxplot av friksjonskoeffisient μ for hver run')
plt.ylabel('μ-verdi')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()