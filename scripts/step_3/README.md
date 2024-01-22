This step creates a summary table of PRDM9 domains presence/absence for selected proteins for every organism. 
First, a markovian model is built from a pre-existing reference alignment for every domain using the hmmbuild command from HMMER. The resulting models can be found in the results/hmm_build directory.
Next, the models for the four domains are used to search for candidates in the proteome of every organism with the hmmsearch command from HMMER. This produces two complementary outputs for every iteration, one with the details of every match found for one domain for every protein, and one with only the best match for every protein. The threshold to be selected as a candidate is 1E-3. This can be modified manually in the rule hmm_search in the snakefile. 
Finally, a summary table is created for every organism using the results of hmmsearch.
All the result files for a given organism are available in the directory named as its accession number in the result directory.

To run this step, choose X, the number of cores to use and execute this command :
    `snakemake -s scripts/step_3/summary_table.smk -cX`