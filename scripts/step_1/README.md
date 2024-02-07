This step gathers important information from the NCBI database to prepare for data download. The query returns which of reference genome, genome annotations and proteome are available to download, and the associated URL address.

Query results are saved in tabular format in the data/resources/organisms_data file, with the following columns:
- Species Name
- Taxid
- Reference genome accession number
- Annotation and proteome availability
- Download URL

The default query gathers Insecta taxa data. This can be changed using the --config parameter in the snakemake command line (eg: --config query=Arachnida), or by modifying the config.json file.

To run this step, choose X, the number of cores to use and execute this command :
    `snakemake -s scripts/step_1/fetch_data.smk -cX`