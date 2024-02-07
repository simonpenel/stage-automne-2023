configfile: "scripts/step_2/config.json"

with open("data/resources/organisms_data") as reader:
    """
    Creates the list of URL that will be used for download
    """
    PATHLIST = []
    ACCESSNB = []
    CUR_LIST = []
    CURATED = [] # Assemblies with annotation and protein sequence
    for line in reader.readlines()[1:]:
        line_data = line.strip().split('\t')
        if line_data[-1] != 'None': # if there is an existing URL
            ACCESSNB.append(line_data[2])
            PATHLIST.append(f"{line_data[-1]}")
            if line_data[3] == 'True': # if genome is curated
                CUR_LIST.append(f"{line_data[-1]}")
                CURATED.append(line_data[2])
                print(line_data[2], line_data[3])

if config["curated_only"] == 1:
    FINAL = CURATED # Accession number list
    PATHLIST = dict(zip(FINAL, CUR_LIST)) # Dictionary with accession number as keys and URLs as values
else:
    FINAL = ACCESSNB
    PATHLIST = dict(zip(FINAL, PATHLIST))

rule all:
    input: 
        expand("data/ncbi/{accession}/protein.faa", accession=CURATED),
        expand("data/ncbi/{accession}/genomic.fna", accession=FINAL),
        expand("data/ncbi/{accession}/genomic.gff", accession=CURATED)


def GetPath(wildcards):
    return(PATHLIST[wildcards.accession])

rule download_protein_data:
    params:
        http_path = GetPath
    input:
        "data/resources/organisms_data"
    output:
        "data/ncbi/{accession}/protein.faa"
    shell:
        """
        cd data/ncbi/{wildcards.accession}/ \
        && wget {params.http_path}_protein.faa.gz \
        && gunzip *.gz \
        && ln -s *.faa protein.faa\
        && makeblastdb -in protein.faa -title protdb -out protdb -dbtype prot -parse_seqids\
        && cd ../../../
        """
        # the blast database is created here to be used during the 4th step 
        # for proteic sequence extraction
        >
rule download_genomic_data:
    params:
        http_path = GetPath
    input:
        "data/resources/organisms_data"
    output:
        "data/ncbi/{accession}/genomic.fna"
    shell:
        """
        cd data/ncbi/{wildcards.accession}/ \
        && wget {params.http_path}_genomic.fna.gz \
        && gunzip *.gz \
        && ln -s *.fna genomic.fna\
        && cd ../../../
        """

rule download_annotation_data:
    params:
        http_path = GetPath
    input:
        "data/resources/organisms_data"
    output:
        "data/ncbi/{accession}/genomic.gff"
    shell:
        """
        cd data/ncbi/{wildcards.accession}/ \
        && wget {params.http_path}_genomic.gff.gz \
        && gunzip *.gz \
        && ln -s *.gff genomic.gff\
        && cd ../../../
        """
