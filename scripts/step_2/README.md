This step manages the download of all available data according to previously gathered information, which can be found in data/resources/organisms_data. 
By default, all reference genomes will be downloaded, along with annotation and protein sequence files should they exist. This can be changed to downloading only curated genomes only (only genomes with annotations and proteomes) using the --config parameter in the snakemake command line (eg: --config curated_only=1), or by modifying the config.json file. It is also possible to comment the corresponding snakemake rules to avoid downloading useless data type.

To run this step, choose X, the number of cores to use and execute this command :
    `snakemake -s scripts/step_2/data_dl.smk -cX`