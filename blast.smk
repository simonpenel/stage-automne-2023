import os

ACCESSNB = [elt for elt in os.listdir('results/') if elt.startswith('GC') == True]

rule all:
    input: expand("results/{accession}/blast_table_{accession}.csv", accession=ACCESSNB)

rule gatekeep:
    priority: 1
    message:
        "Please check you have no file named blastp_summary.txt in the current directory. If you do, please move, rename or delete it to ensure this pipeline operates properly."

rule read_table:
    input:
        "results/{accession}/summary_table_{accession}.csv"
    output:
        "results/{accession}/blast_table_{accession}.csv"
    shell:
        """
        python blastp_analysis.py results/{wildcards.accession}/summary_table_{wildcards.accession}.csv {wildcards.accession}
        """

