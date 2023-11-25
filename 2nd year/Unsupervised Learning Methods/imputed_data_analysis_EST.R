# ANÁLISE COMPLEMENTAR AOS DADOS DO PISA 2018 PARA A ESTÓNIA 
# (COM IMPUTAÇÃO DE OMISSOS, USANDO A BIBLIOTECA "mice" do R)

pacman::p_load(dplyr, haven, psych, corrplot, svglite, skimr, plotrix, 
               sjstats, modeest, cluster, tidyverse, caret, factoextra, 
               mclust, mice, gpairs, naniar)

# ler o rds gerado no outro ficheiro com a imputação de omissos efetuada
imputed_data_est <- readRDS("imputed_data_est.rds")
imputed_data_est_PCA <- imputed_data_est[,1:38]


# dimensão do dataframe e quantidade de omissos
dim(imputed_data_est)
colSums(is.na(imputed_data_est))

# teste de bartlett
cortest.bartlett(imputed_data_est_PCA)

# KMO aceitável de 0.7
KMO(imputed_data_est_PCA)

non_numeric_imp <- sapply(imputed_data_est_PCA, function(x) !is.numeric(x))
num_numeric_imp <- sum(sapply(imputed_data_est_PCA, is.numeric))

data_scaled_imp <- imputed_data_est_PCA[, !non_numeric_imp] %>%
  mutate_if(is.numeric, scale)

cat("Foram estandardizadas",num_numeric_imp,"variáveis numéricas.")


# Assumir que número de componentes = 38
options(max.print=2500)
imp_pc38 <- principal(data_scaled_imp, nfactors=num_numeric_imp, rotate="none", scores=TRUE)

# eingenvalues
round(imp_pc38$values,3)

# screeplot
plot(imp_pc38$values, type = "b", main = "Scree plot for PISA in Estonia", 
     xlab = "Number of PC", ylab = "Eingenvalue")
# Pela screeplot talvez 6 componentes

# verificar loadings
imp_pc38$loadings
# Pela variância acumulada talvez 6 componentes, tal como no outro método


# TESTE para 6 COMPONENTES, sem rotação
imp_pc6 <- principal(data_scaled_imp, nfactors=6, rotate="none")
imp_pc6$loadings
# As componentes parecem ser bastante parecidas com as conseguidas sem imputação,
# mas menos notórias em alguns casos

# Rodar os 6 componentes usando VariMax
imp_pc6r <- principal(data_scaled_imp, nfactors=6, rotate="varimax")
imp_pc6r$loadings
# ao rodarmos o plano dos dados verificamos valores bastante parecidos aos sem imputação, 
# talvez por estarmos a utilizar dados sintéticos gerados a partir de outros
# ao invés de recolhidos por estudantes


# ver comunalidades
round(imp_pc6$communality,2)
# tal como na outra análise, comunalidades todas acima de 0.2/0.3 (maioria mais que 0.4), 
# com exceção do BEINGBULLIED que teve valores de 0.15


###############################################################################

imp_estonia_pca <- data.frame(
  ambition = imp_pc6r$scores[, 1],
  achievement = imp_pc6r$scores[, 2],
  ICT = imp_pc6r$scores[, 3],
  learning_time = imp_pc6r$scores[, 4],
  mental_health = imp_pc6r$scores[, 5],
  support = imp_pc6r$scores[, 6]
)

# head(imp_estonia_pca)

###############################################################################

imp_pc_dist <- dist(imp_estonia_pca)
hclust <- hclust(imp_pc_dist, method='ward.D2')
plot(hclust, hang=-1, labels=FALSE)
# 3 clusters
n_clusters <- 3

groups.h3 <- cutree(hclust, k=n_clusters) 
rect.hclust(hclust, k=n_clusters, border="red")

plot(silhouette(groups.h3, imp_pc_dist))
# cluster hierarquico com 3 clusters

wssplot <- function(xx, nc=15, seed=1234){
  wss <- (nrow(xx)-1)*sum(apply(xx,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(xx, centers=i)$withinss)}
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares")}
wssplot(imp_estonia_pca, nc=10)
# numero de clusters igual ao da outra analise (screeplot)


# K-MEANS
kmeans.k4 <- kmeans(imp_estonia_pca, 4, nstart=100) 
estonia_pca <-  imp_estonia_pca %>% mutate(cluster = kmeans.k4$cluster)

# PAM
imp_std_data <- scale(imp_estonia_pca)
pam.k4 <- pam(imp_std_data, 4)
table(groups.h3,pam.k4$clustering)
clusplot(pam.k4, labels = FALSE, col.p = pam.k4$clustering)








