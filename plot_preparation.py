from ete3 import NCBITaxa
import pandas as pd
import sqlite3
import os

ncbi = NCBITaxa()
tenta_df = []
with open('unratioed_values', 'r+') as reader:
    for line in reader.readlines():
        line = line.strip()
        if line.startswith('>') == True:
            taxid = line.lstrip('>')
            lineage = ncbi.get_lineage(taxid)
            taxonomy = ncbi.get_taxid_translator(lineage)
            species = ncbi.get_taxid_translator([taxid])[int(taxid)]
            superorder = taxonomy[lineage[18]]
        elif line.startswith('<') == True:
            krab = int(line.split('\t')[1])
            ssxrd = int(line.split('\t')[2])
            zf = int(line.split('\t')[3])
        else:
            line = line.split('\t')
            tenta_df.append([taxid, species, superorder, line[0], line[1], line[2], krab, ssxrd, zf])

plot_df = pd.DataFrame(tenta_df, columns=['Taxid', 'Species_name', 'Superorder', 'Protein ID', 'Bit score', 'Ratio', 'KRAB', 'SSXRD', 'ZF'])
plot_df.to_csv('plotdata.csv', sep=';')

# Suppression de la colonne inutile (anciens indexs)
plot_df = plot_df.loc[:, ~plot_df.columns.str.contains('^Unnamed')]

# Lecture des données taxonomiquese t ajout d'une colonne de synthèse des noms d'espèces
taxonomy = pd.read_csv("sorted_taxonomy.csv", sep=",")
for index, row in taxonomy.iterrows():
    last_valid_col = taxonomy.iloc[index].last_valid_index()
    taxonomy.at[index, 'Species_name'] = taxonomy.loc[index, last_valid_col]
taxonomy = taxonomy[['Species_name', 'Accession']]
taxonomy.rename(columns={'Species_name': 'Species_name2'}, inplace=True)

plot_df = plot_df.sort_values(by=['Superorder', 'Species_name']) 

# Sélection des organismes avec les 4 domaines protéiques, et de la protéine avec le meilleur match si nécessaire
plot_df['total_domains'] = 1 + plot_df['KRAB'] + plot_df['SSXRD'] + plot_df['ZF']
plot_df = plot_df[plot_df['total_domains'] == 4]
plot_df['Bit score'] = plot_df['Bit score'].astype(float)
result = plot_df.loc[plot_df.groupby('Species_name')['Bit score'].idxmax()]
# Fusion des 2 dataframes pour avoir les numéros d'accession
conn = sqlite3.connect('fusion.sql') 
taxonomy.to_sql("taxonomy", conn, index=False, if_exists='replace')
result.to_sql("result", conn, index=False, if_exists='replace')
query = 'SELECT *\
        FROM taxonomy t INNER JOIN result r ON t.Species_name2 == r.Species_name'
df_fusion = pd.read_sql(query, conn)
df_fusion = df_fusion.drop(['Species_name2'], axis = 1)
df_fusion.to_csv('PRDM9_data.csv', index= False, sep=';')
os.remove('fusion.sql')

