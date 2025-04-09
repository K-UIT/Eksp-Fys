import pandas as pd
import matplotlib.pyplot as plt

g = 9.81  # tyngdeakselerasjon

def behandle_excel_run(filepath):
    df = pd.read_excel(filepath)
    print("Kolonner funnet:", df.columns)
    
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

    # Histogram
    plt.figure(figsize=(8, 5))
    plt.hist(waa, bins=30, color='skyblue', edgecolor='black')
    plt.title(f'Fordeling av a per Run – {filepath}')
    plt.xlabel('a-verdi')
    plt.ylabel('Antall')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # Beregn snitt og mu
    if not gyldige_a.empty:
        mean_a = gyldige_a.mean()
        mu = 1 / (mean_a * 2 * g)
        print(f"\nFil: {filepath}")
        print(f"Gjennomsnittlig a: {mean_a:.5f}")
        print(f"Friksjonskoeffisient mu: {mu:.5f}")
        return a_df, mean_a, mu
    else:
        print("Ingen gyldige målinger.")
        return a_df, None, None



behandle_excel_run('Måledata 0L.xlsx')
behandle_excel_run('Måledata 0,25L.xlsx')
behandle_excel_run('Måledata 0,55L.xlsx')
