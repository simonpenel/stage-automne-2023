library("ggplot2")
library("plotly")
library("dplyr")

donnees <- read.csv2("plotdata.csv")

donnees <- donnees[, -which(names(donnees) == "X")]
donnees$Ratio=as.numeric(as.character(donnees$Ratio))
donnees$Bit.score=as.numeric(as.character(donnees$Bit.score))


donnees=donnees[order(donnees$Superorder,donnees$Species.name),]
donnees$num=c(1:nrow(donnees))
donnees <- donnees %>%
  mutate(total_domains = 1 + KRAB + SSXRD+ ZF)
donnees <- donnees %>%
  rowwise() %>%
  mutate(
    cols_with_one = paste(names(select(., KRAB, ZF, SSXRD))[c(KRAB, ZF, SSXRD) == 1], collapse = ", ")
  )

# p <- ggplot(data = donnees, aes(x = Ratio, 
#                                 y = num, 
#                                 color = Superorder,
#                                 text = paste("Domains:", cols_with_one))) +
#   geom_point(alpha = (donnees$total_domains / 4)) +
#   labs(title = "Scatter Plot", x = "Score PRDM9/PRDMX", y = "Espèce")
# ggplotly(p)
p <- ggplot(data = donnees, aes(x = Ratio,
                           y = num,
                           text = paste("Species:", Species.name, "\nDomains:", cols_with_one))) +
  geom_point(aes(fill = Superorder,
                 color = I(ifelse(total_domains == 4, "black", "transparent"))),
             alpha = (donnees$total_domains / 4),
             shape = 21) +
  labs(title = "Scatter Plot", x = "Score PRDM9/PRDMX", y = "Espèce")
ggplotly(p)


q <- ggplot(data = donnees, aes(x = Ratio,
                                y = Bit.score,
                                text = paste("Species:", Species.name, 
                                             "\nnum:", num, 
                                             "\nDomains:", cols_with_one))) +
  geom_point(aes(fill = Superorder,
                 color = I(ifelse(total_domains == 2, "black", "transparent"))),
             alpha = (donnees$total_domains / 2),
             shape = 21) +
  labs(title = "Scatter Plot", x = "Score PRDM9/PRDMX", y = "Bit Score")
ggplotly(q)
##################################################################################

# library("ggplot2")
# donnees <- read.csv2("plotdata.csv")
# 
# head(donnees)
# donnees <- donnees[, -which(names(donnees) == "X")]
# donnees$Ratio=as.numeric(as.character(donnees$Ratio))
# donnees=donnees[order(donnees$Superorder,donnees$Species.name),]
# donnees$num=c(1:nrow(donnees))
# 
# p <- ggplot(data = donnees, aes(x = Ratio, y = num, color = Superorder, shape = Superorder)) +
#   geom_point() +
#   labs(title = "Scatter Plot", x = "Score PRDM9/PRDMX", y = "Espèce")
# p
# p + scale_x_continuous(breaks = seq(min(F$Ratio), max(F$Ratio), by = 10))
# 
# D=donnees[order(donnees$Superorder,donnees$Species.name),]
# D$num=c(1:nrow(D))
# D$Ratio=as.numeric(as.character(D$Ratio))
# D$col = "yellow"
# D$col[which(D$Superorder=="Endopterygota")]="red"
# D$col[which(D$Superorder=='Paraneoptera')]="blue"
# D$col[which(D$Superorder=='Polyneoptera')]="green"
# D$col[which(D$Superorder=='Odonata')]="black"
# plot(D$num, D$Ratio, col = D$col, pch=19)
# 
# summary(D)








