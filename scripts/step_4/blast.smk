import os

ACCESSNB = [elt for elt in os.listdir('results/') if elt.startswith('GC') == True]

rule all:
    input:
        "table_results/krab_data.csv",
        "table_results/krabzf_data.csv",
        "table_results/zf_count.csv",
        "table_results/table_prdm9.csv"

rule read_table:
    """
    Reads each summary table and runs a blastp analysis on every candidate
    """
    input:
        "results/{accession}/summary_table_{accession}.csv"
    output:
        "results/{accession}/blastp.txt",
    shell:
        """
        python3 scripts/step_4/blastp_analysis.py results/{wildcards.accession}/summary_table_{wildcards.accession}.csv {wildcards.accession}\
        """

rule summary:
    """
    Concatenation of each proteome blastp results.
    """
    input: 
        expand("results/{accession}/blastp.txt", accession=ACCESSNB)
    output:
        "results/BLASTP_results/blastp_summary.txt"
    shell:
        """
        cat {input} > {output}
        """

rule blastp_results:
    """
    Writing a table from the concatenation
    """
    input:
        "results/BLASTP_results/blastp_summary.txt"
    output:
        "results/BLASTP_results/blastp_results.csv",
    shell:
        """
        python3 scripts/step_4/blastp_table.py\
        """

rule taxonomy:
    """
    Creation of a table associating a genome accession number to its complete taxonomy
    """
    input:
        "results/BLASTP_results/blastp_summary.txt"
    output:
        "data/resources/sorted_taxonomy.csv"
    shell:
        "python3 scripts/step_4/taxonomy.py"

rule create_table:
    """
    Creation of multiple result table using blastp results and hmm search results
    """
    input:
        "results/BLASTP_results/blastp_results.csv",
        "data/resources/sorted_taxonomy.csv"
    output:
        "table_results/krab_data.csv",
        "table_results/krabzf_data.csv",
        "table_results/zf_count.csv",
        "table_results/table_prdm9.csv"
    shell:
        """
        python3 scripts/step_4/krab.py\
        && python3 scripts/step_4/krabzf.py\
        && python3 scripts/step_4/zf_analysis.py\
        && python3 scripts/step_4/table_prdm9.py
        """
