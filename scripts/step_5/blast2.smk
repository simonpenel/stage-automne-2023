rule all:
    input:
        "table_results/krab_data.csv",
        "table_results/krabzf_data.csv",
        "table_results/zf_data.csv",
        "table_results/table_candidats_exclus.csv",
        "table_results/table_prdm9.csv"

rule blastp_results:
    input:
        "results/BLASTP_results/blastp_summary.txt"
    output:
        "results/BLASTP_results/blastp_results.csv",
    shell:
        """
        python scripts/step_4/blastp_table.py\
        """

rule taxonomy:
    input:
        "results/BLASTP_results/blastp_summary.txt"
    output:
        "data/resources/sorted_taxonomy.csv"
    shell:
        "python scripts/step_4/taxonomy.py"

rule create_table:
    input:
        "results/BLASTP_results/blastp_results.csv",
        "data/resources/sorted_taxonomy.csv"
    output:
        "table_results/krab_data.csv",
        "table_results/krabzf_data.csv",
        "table_results/zf_data.csv",
        "table_results/table_candidats_exclus.csv",
        "table_results/table_prdm9.csv"
    shell:
        """
        python scripts/step_4/krab.py\
        && python scripts/step_4/krabzf.py\
        && python scripts/step_4/zf_analysis.py\
        && python scripts/step_4/table_candidats_exclus.py\
        && python scripts/step_4/table_prdm9.py
        """