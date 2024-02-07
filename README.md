# stage-automne-2023
This snakemake pipeline was developped by Adrien Raimbault as a part of a voluntary Master degree internship under the superision of Laurent Duret (LBBE). It is designed to detect the PRDM9 gene in a specified set of proteomes from the NCBI using HMMER and BLAST.  

## Step 1   
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
## Step 2  
This step manages the download of all available data according to previously gathered information, which can be found in data/resources/organisms_data.   

By default, all reference genomes will be downloaded, along with annotation and protein sequence files should they exist. This can be changed to avoid downloading  genomes without annotations and proteomes using the --config parameter in the snakemake command line as such : `--config curated_only=1`, or by modifying the config.json file. It is also possible to comment the corresponding snakemake rules to avoid downloading useless data type.   

To run this step, choose X, the number of cores to use and execute this command :
    `snakemake -s scripts/step_2/data_dl.smk -cX`
## Step 3   
This step creates a summary table of PRDM9 domains presence/absence for selected proteins for every organism.   
 
First, a markovian model is built from a pre-existing reference alignment for every domain using the hmmbuild command from HMMER. The resulting models can be found in the results/hmm_build directory.  

Next, the models for the four domains are used to search for candidates in the proteome of every organism with the hmmsearch command from HMMER. This produces two complementary outputs for every iteration, one with the details of every match found for one domain for every protein, and one with only the best match for every protein. The threshold to be selected as a candidate is 1E-3. This can be modified manually in the rule hmm_search in the snakefile.   

Finally, a summary table is created for every organism using the results of hmmsearch.  

All the result files for a given organism are available in the directory named as its accession number in the result directory.  

To run this step, choose X, the number of cores to use and execute this command :
    `snakemake -s scripts/step_3/summary_table.smk -cX`
## Step 4  
This step runs a BLASTP analysis against the human PRDM family database ('data/PRDM_family_HUMAN') for every previously selected (with hmm_search) organisms and sequences.   

It creates 6 csv format output using the blast results and hmm_search results.  

The first output, blastp_results.csv, is a table formatting of blastp_summary.txt and can be found in the same directory, results/BLASTP_results/. It was built separately for optimisation reasons.    
The five following outputs can be found in the table_results/ directory.  

The second output, krab_data.csv, uses the results of hmm_search for the KRAB domain to create a table, with a line for each species shoxing their reference genome accession number, the list of their proteins having a KRAB domain, and the length of this list.  

The third output, krabzf_data.csv works exactly the same but applied to the zinc finger domain. It also comes with an additionnal column, which shows the list of proteins having at least one KRAB and one ZF domains for each species.  

The fourth output, zf_count.csv, uses the per domain results of hmm_search (results/{accession_number}/hmm_search/domtbl/ZF_domains_summary)  to count the total number of proteins having or more zinc finger domains for each species.   

The fifth and sixth output, table_candidats_exclus.csv and table_prdm9.csv, both have the same formatting:  
- the taxid of the species,  
- the reference genome accession number,  
- the species name,  
- the number of SET doamisn found in the species proteome,  
- the count of proteins with all 4 domains in the gene, and the list of the proteins names,  
- the count of proteins with the KRAB, SET and SSXRD domains in the gene, and the list of the proteins names,  
- the count of proteins with the KRAB, SET and ZF domains in the gene, and the list of the proteins names,  
- the count of proteins with KRAB and SET domains in the gene, and the list of the proteins names.  

To run this step, choose X, the number of cores to use and execute these commands :
    `snakemake -s scripts/step_4/blast.smk -cX`
