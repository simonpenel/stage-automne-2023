library(dplyr)

prdm9_data = read.csv2("table_results/table_prdm9.csv")
taxonomy = read.csv2("data/resources/sorted_taxonomy.csv")
krab_data = read.csv2("table_results/krab_data.csv")
zf_data = read.csv2("table_results/zf_count.csv")

krab_data$KRAB_protein_list <- krab_data$Protein.List
krab_data <- subset(krab_data, select = -Protein.List)
zf_data$Five_or_more_ZF <- zf_data$X5..ZF
zf_data <- subset(zf_data, select = -X5..ZF)

prdm9_data = subset(prdm9_data, select = -c(Taxid, Species_name))
krab_prdm9 <- merge(prdm9_data, krab_data, by="Accession")
krabzf_prdm9 <- merge(krab_prdm9, zf_data, by="Accession")
merged <- merge(taxonomy, krabzf_prdm9, by="Accession")
merged <- subset(merged, select = -c(X, Taxid))

prdm9_stat <- function(dataframe) {
  TOTAL <- nrow(dataframe) 
  Complet <- sum(dataframe$Complete_PRDM9.nb) 
  SET_KRAB_SSXRD <- sum(dataframe$SET.KRAB.SSXRD.nb)
  SET_KRAB_ZF <- sum(dataframe$SET.KRAB.ZF.nb)
  SET_KRAB <- sum(dataframe$SET.KRAB.nb)
  KRAB <- sum(dataframe$KRAB.nb)
  Five_or_more_ZF <- round(mean(dataframe$Five_or_more_ZF))
  
  
  new_table <- data.frame(TOTAL, Complet, SET_KRAB_SSXRD, SET_KRAB_ZF, SET_KRAB, KRAB, Five_or_more_ZF)
  return(new_table)
}

check_taxon_presence <- function(df, taxon) {
  n=ncol(df)
  for(ii in 1:n) {
    sel<-which(df[,ii]==taxon)
    if(length(sel)>0) return(sel)
  }
  warnings(sprintf("WARNING: taxon %s not found", taxon))
  return(NULL)
}

get_sub_df <- function(df, taxons) {
  result_list <- list()
  for (taxon in taxons) {
    #taxon_presence <- apply(df, 1, check_taxon_presence, taxon = taxon)
    taxon_presence<-check_taxon_presence(df,taxon)
    # print(sprintf("taxon %s %d lines", taxon, length(taxon_presence)))
    subset_df <- df[taxon_presence, ]
    result_list[[taxon]] <- prdm9_stat(subset_df)
  }
  result_df <- do.call(rbind, result_list)
  return(result_df)
}

taxon_input <- readline("Liste de clades à étudier (séparés par des virgules): ")
taxons <- unlist(strsplit(taxon_input, ", "))
result_df <- get_sub_df(merged, taxons)
result_df
 merged
