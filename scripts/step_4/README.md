This step runs a BLASTP analysis against the human PRDM family database ('data/PRDM_family_HUMAN') for every previously selected (with hmm_search) organisms and sequences. 
The results are summed up in the blastp_summary.txt file that can be found in the results/BLASTP_results directory, and is written like this:

>116153
<	1	0	0	4
XP_049821907.1	PRDM1
<	1	0	0	0
XP_019877117.2	60.1	1.0770609318996416	PRDM9

The lines starting with the '>' symbol are the taxids. Every line until the next '>' refers to the taxid (species) above.
The other lines function in pairs: 
-the first line, starting with the '<' symbol carry a boolean value  regarding the presence/absence of proteic domains. The order is SET, KRAB, SSXRD and ZF.
-the second line, with no special symbol at the start, is made of the protein ID and the blastp best match. If the best match was PRDM9, the blast bit score and the ratio with the next non-PRDM9 best match are added between the protein ID and the best match (see the example above).

Before running this step, make sure to delete or rename any existing blastp_summary.txt file, as it is created iteratively, over the course of the multiple python script executions (snakemake will run it once for each selected organism) by writing the new lines at the end of the file. If you do not delete it, you will progressively get a bigger and bigger file, with a lot of redundant information, and slow the pipeline execution.
To run this step, choose X, the number of cores to use and execute these commands :
    `rm results/BLASTP_results/blastp_summary.txt` or `mv results/BLASTP_results/blastp_summary.txt new_name`
    `snakemake -s scripts/step_4/blast.smk -cX`