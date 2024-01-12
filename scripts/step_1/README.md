Cette étape a pour but de récupérer les informations importantes pour le pipeline dans les données du NCBI. La requête permet de savoir quelles données sont disponibles au téléchargement parmi la séquence génomique de référence, les annotations du génome et la séquence protéique et d'enregistrer l'URL de téléchargement associée. 
Les résultats sont stockés sous forme tabulaire dans un fichier data/resources/organisms_data délimité par des tabulations, et formatés ainsi : Nom de l'espèce, Numéro de taxon, Numéro d'accession, Disponibilité des fichiers d'annotation et de séquence protéique, URL de téléchargement si elle existe.
Par défaut, la requête demande les informations disponibles pour les insectes. Elle peut être modifiée ponctuellement lors du lancement du pipeline en utilisant le paramètre --config (ex: --config query=Arachnida) ou de manière pérenne en modifiant la valeur de 'query' dans le fichier config.json

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