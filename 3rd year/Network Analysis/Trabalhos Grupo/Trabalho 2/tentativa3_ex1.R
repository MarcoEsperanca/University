library(igraph)

# Função para gerar uma rede aleatória a partir de uma clique inicial
gerar_rede_aleatoria <- function(seed) {
  set.seed(seed)  # Define a semente especificada
  rn1 <- graph.full(10, directed = FALSE)
  x = 10
  
  for (i in 1:191) {
    for (j in 1:3) {
      if (vcount(rn1) >= 200) break
      rn1 <- add_vertices(rn1, 1)
      new <- floor(runif(1, min = 1, max = x))
      nn <- neighbors(rn1, new)
      x = x + 1
      newr <- runif(1)
      
      if (!(new %in% nn)) {
        rn1 <- add_edges(rn1, c(new, x))
      }
      
      if (newr < 0.8) {
        deg <- degree(rn1, new, mode = "all")
        new1 <- floor(runif(1, min = 1, max = deg))
        rn1 <- add_edges(rn1, c(x, nn[new1]))
      } else {
        new2 <- new
        while (new == new2) new2 <- floor(runif(1, min = 1, max = x - 1))
        rn1 <- add_edges(rn1, c(new2, x))
      }
    }
  }
  
  return(rn1)
}



# Função para imprimir métricas de uma rede
imprimir_metricas <- function(rede) {
  avg_distance <- mean_distance(rede)
  coeficiente_clustering <- transitivity(rede)
  deg <- degree(rede, mode = "all")
  ht_network <- mean(deg^2) / mean(deg)^2
  
  
  cat("Distância Média:", avg_distance, "\n")
  cat("Número de vértices (n):", vcount(rede), "\n")
  cat("Coeficiente de Clustering:", coeficiente_clustering, "\n")
}

# Especificar as 10 sementes manualmente
seeds <- c(123, 456, 789, 321, 654, 987, 135, 246, 579, 802)

# Gerar 10 redes aleatórias
rede_list <- lapply(seeds, function(seed) gerar_rede_aleatoria(seed))

# Imprimir métricas para cada rede em rede_list
for (i in 1:length(rede_list)) {
  cat("Rede", i, "\n")
  imprimir_metricas(rede_list[[i]])
  cat("\n")
}
