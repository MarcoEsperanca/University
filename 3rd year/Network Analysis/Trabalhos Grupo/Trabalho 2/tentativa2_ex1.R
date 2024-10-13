library(igraph)

# gera uma clique com 10 nodos
rn1 <- graph.full(10, directed = FALSE)
plot(rn1)
vcount(rn1)
ecount(rn1)

x = 10

set.seed(777)
for (i in 1:191) {
  num_ligacoes_iteracao <- 0  # Contador para ligações em cada iteração
  for (j in 1:3) {
    rn1 <- add_vertices(rn1, 1)
    new <- floor(runif(1, min = 1, max = x))
    nn <- neighbors(rn1, new)
    x = x + 1
    rn1 <- add_edges(rn1, c(new, x))
    num_ligacoes_iteracao <- num_ligacoes_iteracao + 1 
    newr <- runif(1)
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
  print(paste("Iteração", i, "- Número de ligações na iteração:", num_ligacoes_iteracao))
}

plot(rn1, vertex.size = 5, vertex.label = NA)


