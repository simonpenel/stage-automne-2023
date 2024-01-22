import pandas as pd

"""
This script creates a summary table of domain presence absence in genes that are identified as PRDM9 for every organism
"""

taxonomy = pd.read_csv('sorted_taxonomy.csv', sep= ';')
taxonomy = taxonomy[['Taxid', 'Accession']]
donnees = pd.read_csv("plotdata.csv", sep=";")
donnees = donnees.loc[:, ~donnees.columns.str.contains('^Unnamed')]
donnees['boolZF'] = donnees['ZF'].apply(lambda x: 0 if x == 0 else 1)
donnees['Complete_PRDM9'] = ((donnees['SET'] + donnees['KRAB'] + donnees['SSXRD'] + donnees['boolZF'] == 4)).astype(int)
donnees['SET+KRAB+SSXRD'] = ((donnees['Complete_PRDM9'] == 0) & (donnees['KRAB'] + donnees['SSXRD'] == 2)).astype(int)
donnees['SET+KRAB+ZF'] = ((donnees['Complete_PRDM9'] == 0) & (donnees['KRAB'] + donnees['boolZF'] == 2)).astype(int)
donnees['SET+KRAB'] = ((donnees['Complete_PRDM9'] == 0) & (donnees['SET+KRAB+ZF'] == 0) & (donnees['SET+KRAB+SSXRD'] == 0) & (donnees['KRAB'] == 1)).astype(int)
donnees['KRAB+ZF'] = ((donnees['Complete_PRDM9'] == 0) & (donnees['SET+KRAB+ZF'] == 0) & (donnees['SET+KRAB+SSXRD'] == 0) & (donnees['KRAB'] == 1) & (donnees['boolZF'] == 1)).astype(int)

donnees['PRDM9'] = False
for index, row in donnees.iterrows():
    if row['Best_Match'] == 'PRDM9':
        donnees.at[index, 'PRDM9'] = True 
    else:
        donnees.at[index, 'PRDM9'] = False 

prdm9 = donnees[donnees['PRDM9'] == True]

synth = prdm9.groupby(['Taxid', 'Species_name', 'Superorder']).agg({
    'Complete_PRDM9': lambda x: list(prdm9.loc[x.index, 'Protein ID'][prdm9['Complete_PRDM9'] == 1]),
    'SET+KRAB+SSXRD': lambda x: list(prdm9.loc[x.index, 'Protein ID'][prdm9['SET+KRAB+SSXRD'] == 1]),
    'SET+KRAB+ZF': lambda x: list(prdm9.loc[x.index, 'Protein ID'][prdm9['SET+KRAB+ZF'] == 1]),
    'SET+KRAB': lambda x: list(prdm9.loc[x.index, 'Protein ID'][prdm9['SET+KRAB'] == 1]),
    'KRAB+ZF': lambda x: list(prdm9.loc[x.index, 'Protein ID'][prdm9['KRAB+ZF'] == 1])
}).reset_index()

synth['Complete_PRDM9 nb'] = synth['Complete_PRDM9'].apply(len)
synth['SET+KRAB+SSXRD nb'] = synth['SET+KRAB+SSXRD'].apply(len)
synth['SET+KRAB+ZF nb'] = synth['SET+KRAB+ZF'].apply(len)
synth['SET+KRAB nb'] = synth['SET+KRAB'].apply(len)
synth['KRAB+ZF nb'] = synth['KRAB+ZF'].apply(len)

nombre_lignes_SET = donnees[donnees['SET'] == 1].groupby(['Taxid', 'Species_name']).size().reset_index(name='Nb_SET')
synth = synth.merge(nombre_lignes_SET, on=['Taxid', 'Species_name'], how='left')
synth['Nb_SET'] = synth['Nb_SET'].fillna(0).astype(int)

merge = pd.merge(synth, taxonomy, left_on='Taxid', right_on='Taxid', how='inner')
merge = merge.loc[:, ~merge.columns.str.contains('^Unnamed')]
merge = merge[['Taxid', 'Accession', 'Species_name','Superorder', 
               'Nb_SET', 'Complete_PRDM9 nb', 'Complete_PRDM9', 
               'SET+KRAB+SSXRD nb', 'SET+KRAB+SSXRD', 'SET+KRAB+ZF nb', 'SET+KRAB+ZF', 'SET+KRAB nb', 'SET+KRAB']]
merge.to_csv('table_prdm9.csv', sep = ';', index=False)