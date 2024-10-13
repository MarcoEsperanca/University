library(igraph)

# Função para gerar redes aleatórias a partir de um número variável de cliques
generate_random_networks <- function(num_cliques, iterations) {
  initial_network <- graph.full(n = num_cliques, directed = FALSE)
  
  random_walk_model <- function(network, iterations) {
    for (i in 1:iterations) {
      num_new_nodes <- 1  # Número de nós a serem adicionados a cada iteração
      network <- add_vertices(network, num_new_nodes)
      new_node <- vcount(network)  # Obtém o índice do novo nó adicionado
      
      # Adiciona 3 ligações a partir do novo nó
      for (j in 1:3) {
        neighbors <- sample(1:vcount(network), 1)  # Seleciona um nó aleatório da rede
        network <- add_edges(network, c(new_node, neighbors))
      }
    }
    return(network)
  }
  
  num_networks <- 10
  random_networks <- lapply(1:num_networks, function(i) {
    set.seed(i)  # Define uma semente diferente para cada rede gerada
    random_walk_model(initial_network, iterations = iterations)
  })
  
  results <- list()
  
  for (i in 1:num_networks) {
    network <- random_networks[[i]]
    
    avg_distance <- mean_distance(network)
    log_nodos <- log10(vcount(network))
    coeficiente_clustering <- transitivity(network)
    deg <- degree(network, mode = "all")
    ht_network <- mean(deg^2)/mean(deg)^2
    
    hubs <- ifelse(ht_network > 1.5, which(deg >= quantile(deg, 0.95)), NA)
    
    results[[i]] <- list(
      Network = network,
      `Avg Distance` = avg_distance,
      `Log Nodes` = log_nodos,
      `Clustering Coefficient` = coeficiente_clustering,
      `Heterogeneity` = ht_network,
      Hubs = hubs
    )
  }
  
  return(results)
}

# Função para imprimir os resultados de forma organizada
print_results <- function(results_list) {
  for (i in seq_along(results_list)) {
    cat("Rede", i, ":\n")
    result <- results_list[[i]]
    
    cat("Distância Média:", result$`Avg Distance`, "\n")
    cat("Logaritmo do número de nodos:", result$`Log Nodes`, "\n")
    cat("Coeficiente de Clustering:", result$`Clustering Coefficient`, "\n")
    cat("Heterogeneidade:", result$`Heterogeneity`, "\n")
    
    hubs <- result$Hubs
    if (!is.na(hubs)) {
      cat("Hubs (nós com alta conectividade):", hubs, "\n\n")
    } else {
      cat("Esta rede não é suscetível à existência de hubs.\n\n")
    }
  }
}

# Gerar redes aleatórias com 10 cliques
results_10 <- generate_random_networks(10, iterations = 191)

# Gerar redes aleatórias com 20 cliques
results_20 <- generate_random_networks(20, iterations = 191)

# Imprimir resultados de forma organizada
cat("Resultados para a rede com 10 cliques:\n")
print_results(results_10)

cat("\nResultados para a rede com 20 cliques:\n")
print_results(results_20)
