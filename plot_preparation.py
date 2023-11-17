from ete3 import NCBITaxa
import pandas as pd

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
            tenta_df.append([taxid, species, superorder, line[0], line[1], krab, ssxrd, zf])

plot_df = pd.DataFrame(tenta_df, columns=['Taxid', 'Species name', 'Superorder','Bit score', 'Ratio', 'KRAB', 'SSXRD', 'ZF'])
plot_df.to_csv('plotdata.csv', sep=';')

