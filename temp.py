from ete3 import NCBITaxa
import pandas as pd

data = pd.read_csv('ratio_values', header=None, names=['valeur'])
ncbi = NCBITaxa()
tenta_df = []
with open('ratio_values', 'r+') as reader:
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
            tenta_df.append([taxid, species, superorder, line, krab, ssxrd, zf])

plot_df = pd.DataFrame(tenta_df, columns=['Taxid', 'Species name', 'Superorder', 'Ratio', 'KRAB', 'SSXRD', 'ZF'])
pd.set_option("display.max_rows", None)
plot_df.to_csv('plotdata.csv', sep=';')



with open('ratio_values', 'r+') as reader:
    data = []
    for line in reader.readlines():
        line = line.strip()
        if line.startswith('>') == True:
            taxid = line.lstrip('>')
            lineage = ncbi.get_lineage(taxid)
            taxonomy = ncbi.get_taxid_translator(lineage)
            data.append([taxid]+[taxonomy[k] for k in lineage])
columns = ['Taxid']+ [str(i) for i in range(max([len(data[j]) for j in range(len(data))])-1)]
print(len(columns))

sorted_tax = pd.DataFrame(data, columns=columns)
sorted_tax.columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

sorted_tax = sorted_tax.sort_values(by=columns)
# sorted_tax
sorted_tax.to_csv('sorted_taxonomy.csv', sep= ';')
