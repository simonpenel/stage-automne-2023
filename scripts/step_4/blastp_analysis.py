import sys
import os
import pandas as pd

"""
This script extracts the sequence selected by hmm search for an organism and runs a blastp analysis against the Human PRDM genes family. If the best match is PRDM9, 
the value is saved and compared to the next best non-PRDM9 match.
The ouput file is named blastp_summary.txt and contains the taxid, the best PRDM match, the presence/absence data for every proteic domain, the bit score of the blastp
if the best match is PRDM9 and the ratio with the second best non-PRDM9 match.
"""

df = pd.read_csv(sys.argv[1], sep=';')
accession = sys.argv[2]

with open(f"results/{accession}/blastp.txt", 'w') as writer:
    string = ''
    os.system(f"mkdir -p data/ncbi/{accession}/SET_sequences/")
    os.system(f"mkdir -p data/ncbi/{accession}/SET_blastp/")
    for index, row in df.iterrows():
        taxid = f">{df['Taxid'].iloc[0]}\n"
        set = 0
        krab = 0
        ssxrd = 0
        zf = 0
        if row['Nb SET domains'] != 0: 
            set = 1
        if row['Nb KRAB domains'] != 0: 
            krab = 1
        if row['Nb SSXRD domains'] != 0:
            ssxrd = 1
        if row['Nb ZF domains'] != 0:
            zf = row['Nb ZF domains']
        prot = f"<\t{set}\t{krab}\t{ssxrd}\t{zf}\n"
        print(f"Run blastdbcmd -db data/ncbi/{accession}/protdb -entry {row['SeqID']} -range {int(row['SET domain start'])}-{int(row['SET domain end'])} -out data/ncbi/{accession}/SET_sequences/{row['SeqID']}.fa")
        ret = os.system(f"blastdbcmd -db data/ncbi/{accession}/protdb -entry {row['SeqID']} -range {int(row['SET domain start'])}-{int(row['SET domain end'])} -out data/ncbi/{accession}/SET_sequences/{row['SeqID']}.fa")
        if ret > 0 :
            sys.exit("Error during blastdbcmd")
        print(f"Run blastp -db data/PRDM_family_HUMAN/prdm_family -outfmt 7 -query data/ncbi/{accession}/SET_sequences/{row['SeqID']}.fa -out data/ncbi/{accession}/SET_blastp/{row['SeqID']}")
        ret = os.system(f"blastp -db data/PRDM_family_HUMAN/prdm_family -outfmt 7 -query data/ncbi/{accession}/SET_sequences/{row['SeqID']}.fa -out data/ncbi/{accession}/SET_blastp/{row['SeqID']}")
        if ret > 0 :
            sys.exit("Error during blastp")
        with open(f"data/ncbi/{accession}/SET_blastp/{row['SeqID']}") as reader:
            prot_id = row['SeqID']
            lines = reader.readlines()
            prdm_match = lines[5].split()[1].split('_')[0]
            df.at[index, 'Best Match'] = lines[5].split()[1].split('_')[0] # Best match Prdm number
            if prdm_match == 'PRDM9': # if it is prdm9, save the score and compare it to the next non-prdm9 best match
                df.at[index, 'Bit Score'] = float(lines[5].split()[-1])
                j = 1
                while lines[5 + j].split()[1].split('_')[0] == 'PRDM9': 
                    j += 1
                df.at[index, 'Score ratio'] = float(lines[5].split()[-1])/float(lines[5 + j].split()[-1])
                string += f"{prot}{prot_id}\t{float(lines[5].split()[-1])}\t{float(lines[5].split()[-1])/float(lines[5 + j].split()[-1])}\t{prdm_match}\n"
            else:
                string += f"{prot}{prot_id}\t{prdm_match}\n"
    df.to_csv(f"results/{accession}/summary_table_{accession}.csv", sep=';')
    writer.write(taxid + string)  
