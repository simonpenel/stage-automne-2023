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
- the number of SET domains found in the species proteome,  
- the count of proteins with all 4 domains in the gene, and the list of the proteins names,  
- the count of proteins with the KRAB, SET and SSXRD domains in the gene, and the list of the proteins names,  
- the count of proteins with the KRAB, SET and ZF domains in the gene, and the list of the proteins names,  
- the count of proteins with KRAB and SET domains in the gene, and the list of the proteins names.  

To run this step, choose X, the number of cores to use and execute these commands :
    `snakemake -s scripts/step_4/blast.smk -cX`
