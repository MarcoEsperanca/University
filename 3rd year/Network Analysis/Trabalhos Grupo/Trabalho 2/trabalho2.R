# Instale o pacote igraph se ainda não estiver instalado
# install.packages("igraph")

library(igraph)

# Criação da clique inicial com 10 nós
initial_network <- graph.full(n = 10, directed = FALSE)

# Criação de clique inicial com 20 nós
initial_network_20 <- graph.full(n = 20, directed = FALSE)

# Função para adicionar nós e arestas baseado no modelo de Passeio Aleatório
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



# Gera 10 redes aleatórias a partir da clique inicial
num_networks <- 10
random_networks <- lapply(1:num_networks, function(i) {
  set.seed(i)  # Define uma semente diferente para cada rede gerada
  random_walk_model(initial_network, iterations = 191)
})


print("Resultados para a rede com 10 cliques: ")

# Caracterização das redes geradas
for (i in 1:num_networks) {
  cat("Rede", i, ":\n")
  network <- random_networks[[i]]
  
  # Calcula a distância média
  avg_distance <- mean_distance(network)
  cat("Distância Média:", avg_distance, "\n")
  
  # logaritmo do número de nodos
  log_nodos <- log10(vcount(network))
  cat("Logaritmo do número de nodos:", log_nodos, "\n")
  
  # Calcula o coeficiente de clustering
  coeficiente_clustering <- transitivity(network)

  cat("Coeficiente de Clustering:", coeficiente_clustering, "\n")
  
  # Identifica hubs
  deg <- degree(network, mode = "all")
  ht_network <- mean(deg^2)/mean(deg)^2
  cat("Heterogeneidade:", ht_network, "\n")
  
  # se a heterogeneidade for maior que 1.5, a rede tem hubs
  
  if (ht_network > 1.5) {
    hubs <- which(deg >= quantile(deg, 0.95))
    cat("Hubs (nós com alta conectividade):", hubs, "\n\n")
  } else {
    cat("Esta rede não é suscetível à existência de hubs.\n\n")
  }

  cat("Hubs (nós com alta conectividade):", which(hubs >= quantile(hubs, 0.95)), "\n\n")
}


# Gera 10 redes aleatórias a partir da clique com 20 nodos
num_networks <- 10
random_networks <- lapply(1:num_networks, function(i) {
  set.seed(i)  # Define uma semente diferente para cada rede gerada
  random_walk_model(initial_network_20, iterations = 191)
})


print("Resultados para a rede com 20 cliques: ")



# Caracterização das redes geradas
for (i in 1:num_networks) {
  cat("Rede", i, ":\n")
  network <- random_networks[[i]]
  
  # Calcula a distância média
  avg_distance <- mean_distance(network)
  cat("Distância Média:", avg_distance, "\n")
  
  # logaritmo do número de nodos
  log_nodos <- log10(vcount(network))
  cat("Logaritmo do número de nodos:", log_nodos, "\n")
  
  # Calcula o coeficiente de clustering
  coeficiente_clustering <- transitivity(network)
  
  cat("Coeficiente de Clustering:", coeficiente_clustering, "\n")
  
  # Identifica hubs
  deg <- degree(network, mode = "all")
  ht_network <- mean(deg^2)/mean(deg)^2
  cat("Heterogeneidade:", ht_network, "\n")
  
  # se a heterogeneidade for maior que 1.5, a rede tem hubs
  
  if (ht_network > 1.5) {
    hubs <- which(deg >= quantile(deg, 0.95))
    cat("Hubs (nós com alta conectividade):", hubs, "\n\n")
  } else {
    cat("Esta rede não é suscetível à existência de hubs.\n\n")
  }
  
  cat("Hubs (nós com alta conectividade):", which(hubs >= quantile(hubs, 0.95)), "\n\n")
}






