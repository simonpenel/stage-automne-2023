line = "Dryadula phaetusa	34742	GCA_032432895.1	False	False	https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/032/432/895/GCA_032432895.1_Dpha.assembly.v1.2/GCA_032432895.1_Dpha.assembly.v1.2"


line_data = line.strip().split('\t')
print(line_data[3])