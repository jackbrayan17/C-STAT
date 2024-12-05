import pandas as pd
import numpy as np
import statsmodels.api as sm

# Charger la base de données
file_path = "Base.xlsx"  # Remplacez par le chemin vers votre fichier
df = pd.read_excel(file_path)

# Variables à inclure dans le modèle
variables_log = [
    "Echanges commerciaux",
    "PIB-Nigeria",
    "PIB-Cameroun",
    "Population-Nigeria",
    "Population-Cameroun",
    "TransportInfrast-Cameroun",
    "IDE-Cameroun",
    "Ouvcom-Cameroun",
    "Inflation-Cameroun",
    "Urbanisation-Cameroun",
    "M2-Cameroun",
    "Créditdomestic-Cameroun",
    "goveffectivness-Cameroun",
    "FBCF-Cameroun",
    "TransportInfrast-Nigeria",
    "IDE-Nigeria",
    "Ouvcom-Nigeria",
    "Inflation-Nigeria",
    "Urbanisation-Nigeria",
    "M2-Nigeria",
    "Créditdomestic-Nigeria",
    "goveffectivness-Nigeria",
    "FBCF-Nigeria",
    "VAM-Cameroun",
    "Totter-Cameroun",
    "VAM-Nigeria",
    "Totter-Nigeria"
]

# Transformation logarithmique
df_log = df.copy()
for var in variables_log:
    if var in df.columns:
        df_log[f"ln_{var}"] = np.log(df[var])

# Préparation des variables pour le modèle
X = df_log[["ln_PIB-Nigeria", "ln_PIB-Cameroun", "ln_Population-Nigeria", "ln_Population-Cameroun"]]
y = df_log["ln_Echanges commerciaux"]

# Ajout de la constante au modèle
X = sm.add_constant(X)

# Estimation du modèle
model = sm.OLS(y, X).fit()

# Résultats du modèle
summary = model.summary()
print(summary)

# Sauvegarder les données transformées dans un fichier Excel
output_file = "Transformed_Data_and_Results.xlsx"

# Écriture des données transformées et des résultats
with pd.ExcelWriter(output_file) as writer:
    df_log.to_excel(writer, sheet_name="Transformed Data", index=False)
    # Sauvegarder le résumé du modèle comme texte dans une nouvelle feuille
    summary_df = pd.DataFrame(summary.tables[1].data)
    summary_df.to_excel(writer, sheet_name="Regression Results", index=False, header=False)

print(f"Résultats sauvegardés dans {output_file}")
