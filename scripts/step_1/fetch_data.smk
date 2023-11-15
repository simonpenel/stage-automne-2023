configfile: "scripts/step_1/config.json"

rule all:
    input:"data/resources/organisms_data"

rule ncbi_query:
    output:
        "data/resources/ncbi_extraction"
    params:
        query = config['query']
    shell:
        "esearch -db assembly -query {params.query} | efetch -format docsum  > {output}"

rule frauder_le_xml:
    input:
        "data/resources/ncbi_extraction"
    output:
        "data/resources/rooted_extraction"
    shell:
        """
        python scripts/step_1/xml_rewrite.py {input} {output}\
        && rm {input}
        """

rule data_analysis:
    input:
        "data/resources/rooted_extraction"
    output:
        "data/resources/organisms_data"
    shell:
        "python scripts/step_1/xml_reader.py {input} {output}"
