import os

ACCESSNB = [elt for elt in os.listdir('results/') if elt.startswith('GC') == True]

rule all:
    input: expand("results/{accession}/blast_table_{accession}.csv", accession=ACCESSNB)

rule read_table:
    input:
        "results/{accession}/summary_table_{accession}.csv"
    output:
        "results/{accession}/blast_table_{accession}.csv"
    shell:
        """
        python sum_up_ratios.py results/{wildcards.accession}/summary_table_{wildcards.accession}.csv {wildcards.accession}
        """
#         && awk '/^>/ {sub(">", "", $1); print $1}' ratio_values > taxid.txt\

