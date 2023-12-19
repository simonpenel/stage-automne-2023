from ete3 import NCBITaxa
import pandas as pd
import sqlite3
import os

ncbi = NCBITaxa()
tenta_df = []
with open('blastp_summary.txt', 'r+') as reader:
    for line in reader.readlines():
        line = line.strip()
        if line.startswith('>') == True:
            taxid = line.lstrip('>')
            lineage = ncbi.get_lineage(taxid)
            taxonomy = ncbi.get_taxid_translator(lineage)
            species = ncbi.get_taxid_translator([taxid])[int(taxid)]
            superorder = taxonomy[lineage[18]]
        elif line.startswith('<') == True:
            set = int(line.split('\t')[1])
            krab = int(line.split('\t')[2])
            ssxrd = int(line.split('\t')[3])
            zf = int(line.split('\t')[4])
        else:
            line = line.split('\t')
            if len(line) == 2:
                prot_id = line[0]
                bit_score = 0
                ratio = 0
                match = line[-1]
            else:                
                prot_id = line[0]
                bit_score = line[1]
                ratio = line[2]
                match = line[-1]
            tenta_df.append([taxid, species, superorder, prot_id, bit_score, ratio, set, krab, ssxrd, zf, match])

plot_df = pd.DataFrame(tenta_df, columns=['Taxid', 'Species_name', 'Superorder', 'Protein ID', 'Bit score', 'Ratio', 'SET', 'KRAB', 'SSXRD', 'ZF', 'Best_Match'])

# Suppression de la colonne inutile (anciens indexs)
plot_df = plot_df.loc[:, ~plot_df.columns.str.contains('^Unnamed')]
plot_df.to_csv('plotdata.csv', sep=';')

# Lecture des données taxonomiques et ajout d'une colonne de synthèse des noms d'espèces
taxonomy = pd.read_csv("sorted_taxonomy.csv", sep=";")
for index, row in taxonomy.iterrows():
    last_valid_col = taxonomy.iloc[index].last_valid_index()
    taxonomy.at[index, 'Species_name'] = taxonomy.loc[index, last_valid_col]
taxonomy = taxonomy[['Accession', 'Species_name']]
taxonomy.rename(columns={'Species_name': 'Species_name2'}, inplace=True)

plot_df = plot_df.sort_values(by=['Superorder', 'Species_name']) 

# # Sélection des organismes avec les 4 domaines protéiques, et de la protéine avec le meilleur match si nécessaire
# plot_df['total_domains'] = plot_df['SET'] + plot_df['KRAB'] # + plot_df['SSXRD'] + plot_df['ZF']
# plot_df = plot_df[plot_df['total_domains'] == 2]
# plot_df['Bit score'] = plot_df['Bit score'].astype(float)
# result = plot_df.loc[plot_df.groupby('Species_name')['Bit score'].idxmax()]
# # Fusion des 2 dataframes pour avoir les numéros d'accession
# conn = sqlite3.connect('fusion.sql') 
# taxonomy.to_sql("taxonomy", conn, index=False, if_exists='replace')
# result.to_sql("result", conn, index=False, if_exists='replace')
# query = 'SELECT *\
#         FROM taxonomy t INNER JOIN result r ON t.Species_name2 == r.Species_name'
# df_fusion = pd.read_sql(query, conn)
# df_fusion = df_fusion.drop(['Species_name2'], axis = 1)
# df_fusion.to_csv('PRDM9_data.csv', index= False, sep=';')
# os.remove('fusion.sql')

# os.system(f"mkdir -p test_seq_pour_align/")
# for index, row in df_fusion.iterrows():
#     accession = row['Accession']
#     protein_id = row['Protein ID']
#     os.system(f"blastdbcmd -db data/ncbi/{accession}/protdb -entry {protein_id} -out test_seq_pour_align/{protein_id}.fa")
        
