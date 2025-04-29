import pandas as pd
import matplotlib.pyplot as plt

g = 9.81  # tyngdeakselerasjon

def behandle_excel_run(filepath):
    df = pd.read_excel(filepath)
    #print("Kolonner funnet:", df.columns)
    
    gjennomsnittlige_as = []  # én gjennomsnittlig 'a' per run
    waa = []
    num_runs = df.shape[1] // 3  # én run = 3 kolonner

    for i in range(num_runs):
        try:
            t_col = df.columns[i*3]
            x_col = df.columns[i*3 + 1]
            v_col = df.columns[i*3 + 2]

            run_df = df[[t_col, x_col, v_col]].copy()
            run_df.columns = ['t', 'x', 'v']

            # Finn maks fart
            v_max_index = run_df['v'].abs().idxmax()

            # Ta ut snittdata etter maks fart og til nær stopp
            subset = run_df.iloc[v_max_index:].reset_index(drop=True)
            subset = subset[subset['v'] < -0.01].reset_index(drop=True)

            a_vals = []
            for j in range(len(subset) - 1):
                v1 = subset.loc[j, 'v']
                v2 = subset.loc[j + 1, 'v']
                x1 = subset.loc[j, 'x']
                x2 = subset.loc[j + 1, 'x']
                delta_x = x2 - x1
                if delta_x != 0:
                    a = (v2**2 - v1**2) / delta_x
                    a_vals.append(a)
                    waa.append(a)
            if len(a_vals) > 1:
                a_mean = sum(a_vals[1:]) / len(a_vals[1:])  # hopp over første
                gjennomsnittlige_as.append(a_mean)
            else:
                gjennomsnittlige_as.append(None)  # tom run

        except Exception as e:
            print(f"Feil i run #{i+1}: {e}")
            gjennomsnittlige_as.append(None)

    # Konverter til DataFrame
    a_df = pd.DataFrame({'Run': list(range(1, num_runs + 1)), 'a': gjennomsnittlige_as})
    gyldige_a = a_df['a'].dropna()

    all_a = pd.DataFrame({"at": waa})["at"].dropna()

    # Histogram
    plt.figure(figsize=(8, 5))
    plt.hist(all_a, bins=50, color='skyblue', edgecolor='black')
    plt.title(f'Fordeling av a per Run – {filepath}')
    plt.xlabel('a-verdi')
    plt.ylabel('Antall')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # Beregn snitt og mu
    if not gyldige_a.empty:
        mean_a = gyldige_a.mean()
        mu = mean_a / (2 * g)
        print(f"\nFil: {filepath}")
        print(f"Gjennomsnittlig a: {mean_a:.5f}")
        print(f"Friksjonskoeffisient mu: {mu:.5f}")
        return a_df, mean_a, mu, all_a
    else:
        print("Ingen gyldige målinger.")
        return a_df, None, None



a,b,c,R1=behandle_excel_run('Måledata 0L.xlsx')
a,b,c,R2=behandle_excel_run('Måledata 0,25L.xlsx')
a,b,c,R3=behandle_excel_run('Måledata 0,55L.xlsx')



import numpy as np

# Beregn gjennomsnitt og standardavvik for hvert datasett
mean_R1 = R1.mean()
std_R1 = R1.std(ddof=1)

mean_R2 = R2.mean()
std_R2 = R2.std(ddof=1)

mean_R3 = R3.mean()
std_R3 = R3.std(ddof=1)

print(f"0L:     mean = {mean_R1:.5f}, std = {std_R1:.5f}")
print(f"0.25L:  mean = {mean_R2:.5f}, std = {std_R2:.5f}")
print(f"0.55L:  mean = {mean_R3:.5f}, std = {std_R3:.5f}")

# Vekter: 1 / varians
w1 = 1 / std_R1**2
w2 = 1 / std_R2**2
w3 = 1 / std_R3**2

# Vektet gjennomsnitt
weighted_mean = (w1 * mean_R1 + w2 * mean_R2 + w3 * mean_R3) / (w1 + w2 + w3)

# Kombinert standardavvik
weighted_std = np.sqrt(1 / (w1 + w2 + w3))

print(f"\nVektet gjennomsnitt alpha: {weighted_mean:.5f}")
print(f"\nVektet gjennomsnitt mu: {weighted_mean/(2*g):.5f}")
print(f"Vektet standardavvik: {weighted_std:.5f}")


# Lager stacked histogram igjen
plt.figure(figsize=(8, 5))
plt.hist([R1, R2, R3], bins=200, stacked=True, label=['0L', '0,25L', '0,55L'],
         color=['skyblue', 'lightgreen', 'salmon'], edgecolor='black')

# Legg til linje for vektet gjennomsnitt
plt.axvline(weighted_mean, color='black', linestyle='-', linewidth=2, label='Vektet gjennomsnitt')

# Legg til stiplete linjer for standardavvik
plt.axvline(weighted_mean + weighted_std, color='black', linestyle='--', linewidth=1.5, label='+1 std.avvik')
plt.axvline(weighted_mean - weighted_std, color='black', linestyle='--', linewidth=1.5, label='-1 std.avvik')

# Legg til generell info
plt.title('Fordeling av a per Run – stacked')
plt.xlabel('a-verdi')
plt.ylabel('Antall')
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.show()



# --- NYTT: Konverter a-verdier til mu-verdier ---
R1_mu = R1 / (2 * g)
R2_mu = R2 / (2 * g)
R3_mu = R3 / (2 * g)

# Beregn gjennomsnitt og standardavvik for mu-verdier
mean_R1 = R1_mu.mean()
std_R1 = R1_mu.std(ddof=1)

mean_R2 = R2_mu.mean()
std_R2 = R2_mu.std(ddof=1)

mean_R3 = R3_mu.mean()
std_R3 = R3_mu.std(ddof=1)

print(f"0L:     mean = {mean_R1:.5f}, std = {std_R1:.5f}")
print(f"0.25L:  mean = {mean_R2:.5f}, std = {std_R2:.5f}")
print(f"0.55L:  mean = {mean_R3:.5f}, std = {std_R3:.5f}")

# Vekter: 1 / varians
w1 = 1 / std_R1**2
w2 = 1 / std_R2**2
w3 = 1 / std_R3**2

# Vektet gjennomsnitt
weighted_mean = (w1 * mean_R1 + w2 * mean_R2 + w3 * mean_R3) / (w1 + w2 + w3)

# Kombinert standardavvik
weighted_std = np.sqrt(1 / (w1 + w2 + w3))

print(f"\nVektet gjennomsnitt (mu): {weighted_mean:.5f}")
print(f"Vektet standardavvik (mu): {weighted_std:.5f}")

# --- PLOTTING ---

plt.figure(figsize=(8, 5))
plt.hist([R1_mu, R2_mu, R3_mu], bins=200, stacked=True, label=['0L', '0,25L', '0,55L'],
         color=['skyblue', 'lightgreen', 'salmon'], edgecolor='black')

# Legg til linjer
plt.axvline(weighted_mean, color='black', linestyle='-', linewidth=2, label='Vektet gjennomsnitt')
plt.axvline(weighted_mean + weighted_std, color='black', linestyle='--', linewidth=1.5, label='+1 std.avvik')
plt.axvline(weighted_mean - weighted_std, color='black', linestyle='--', linewidth=1.5, label='-1 std.avvik')

# Tittel og akser
plt.title('Fordeling av friksjonskoeffisient μ per Run – stacked')
plt.xlabel('μ-verdi')
plt.ylabel('Antall')
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.show()


def evaluer_forventet_vs_målt(mu, mu_std, filepaths):
    g = 9.81  # m/s²
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
                forventet_l_std = forventet_l * (mu_std / mu)

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
    plt.figure(figsize=(10, 6))

    run_ids = resultater_df.index + 1  # Nummerering av runs
    avvik = resultater_df['Avvik (m)']
    usikkerhet = resultater_df['Usikkerhet (m)']

    # Plot avvik som punkter
    plt.errorbar(run_ids, avvik, yerr=usikkerhet, fmt='o', color='black',
                 ecolor='red', elinewidth=1.5, capsize=4, label='Avvik med usikkerhet')

    # Nullinje for referanse
    plt.axhline(0, color='blue', linestyle='--', linewidth=2, label='Forventet (0-avvik)')

    plt.title('Forskjell mellom målt og forventet lengde')
    plt.xlabel('Måleforsøk (Run)')
    plt.ylabel('Avvik (målt - forventet) [m]')
    plt.grid(True)
    plt.legend()
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
