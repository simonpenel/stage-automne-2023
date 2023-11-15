from ete3 import NCBITaxa
ncbi = NCBITaxa()

with open('taxid.txt') as reader:
    data_list = [elt for elt in reader.readlines()]

# taxid2name = ncbi.get_taxid_translator(data_list)
# print(taxid2name)

for elt in data_list:
    lineage = ncbi.get_lineage(elt)
    names = ncbi.get_taxid_translator(lineage)
    print(names[lineage[18]])
# print(lineage)
# print(names)