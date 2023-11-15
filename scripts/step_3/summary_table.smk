import os
ACCESSNB = [elt for elt in os.listdir('data/ncbi/') if elt.startswith('GC') == True]

DOMAIN = ['KRAB', 'SET', 'SSXRD', 'ZF']

rule all:
    input: expand("results/{accession}/summary_table_{accession}.csv", accession=ACCESSNB)

rule hmm_build:
    input:
        "data/ref_align/Prdm9_Metazoa_Reference_alignment/Domain_{domain}_ReferenceAlignment.fa"
    output:
        "results/hmm_build/{domain}.hmm"
    shell:
        "hmmbuild {output} {input}"

rule hmm_search:
    input:
        model="results/hmm_build/{domain}.hmm",
        protein="data/ncbi/{accession}/protein.faa"
    output:
        table = "results/{accession}/hmm_search/tbl/{domain}",
        domains = "results/{accession}/hmm_search/domtbl/{domain}_domains"
    shell:
        "hmmsearch -E 1E-3 --domE 1E-3 --tblout {output.table} --domtblout {output.domains} --noali {input.model} {input.protein}"

rule tbl_processing:
    input:
        "results/{accession}/hmm_search/tbl/{domain}"
    output:
        "results/{accession}/hmm_search/tbl/{domain}_processed"
    shell:
        "python scripts/step_3/hmmsearch_parser.py -i {input} -o {output}"

rule domain_processing:
    input:
        "results/{accession}/hmm_search/tbl/{domain}_processed",
        domain_data="results/{accession}/hmm_search/domtbl/{domain}_domains"
    output:
        processed="results/{accession}/hmm_search/domtbl/{domain}_domains_processed",
        summary="results/{accession}/hmm_search/domtbl/{domain}_domains_summary"
    shell:
       "python scripts/step_3/domain_parser.py -i {input.domain_data} -o {output.processed} -s {output.summary}"


def domain_done(wildcards):
    return expand("results/" + wildcards.accession + "/hmm_search/domtbl/{domain}_domains_summary" , domain=DOMAIN)

rule table_editing:
    input:
        domain_done
    output:
        "results/{accession}/summary_table_{accession}.csv"
    shell:
        "python scripts/step_3/table_builder.py -a {wildcards.accession} -o {output}"
