library(igraph)

rede <- read.graph("trab_links.txt", format = c("edgelist"), directed=F)
plot(rede)


# dimensao da rede

# vertices
vcount(rede)

# arestas
ecount(rede)

# densidade

graph.density(rede)

# grau medio

mean(degree(rede))


# distribuicao de graus

degree_distribution(rede)


# verificação se a rede é conexa
# caso não seja indica-se o tamanho mínimo e máximo da componente conexa

is_connected <- is.connected(rede)
print(is_connected)

if (!is_connected) {

  num_components <- length(components(rede))
  print(num_components)
  
  component_sizes <- sizes(components(rede))
  min_size <- min(component_sizes)
  max_size <- max(component_sizes)
  print(paste("Tamanho mínimo da componente conexa:", min_size))
  print(paste("Tamanho máximo da componente conexa:", max_size))
}

# Associação de grau

assortativity_degree(rede)

# media caminhos mais curtos

# 7.914034
mean_distance(rede)

# 0.3453069
log(10, vcount(rede))

# Desta forma, pode-se concluir que a distância média não é pequena,
# pois é bastante diferente do logaritmo do número de nós na rede.


# diametro

diameter(rede)


# Uma distância média de 7.91 pode ser considerada moderada, 
# enquanto um diâmetro de 21 indica que há um par de nós na rede que está relativamente mais distante, 
# mas em geral, a rede possui uma média de distância moderada entre os nós.

# Esses valores podem variar dependendo do tamanho da rede e da natureza dos contatos sociais, 
# mas sugerem que, em média, os habitantes na zona residencial estão relativamente próximos uns dos outros, 
# enquanto ainda há uma certa distância entre os pares mais distantes.


# Estudo da existência de triângulos na rede

transitivity(rede, type = "global")

triangles(rede)

# Obter a matriz de adjacência
adj_matrix <- as.matrix(get.adjacency(rede))

# Calcular o número de triângulos
num_triangles <- sum(adj_matrix %*% adj_matrix %*% adj_matrix) / 6
print(num_triangles)

# Calcular o número de triângulos fechados

num_closed_triangles <- sum(diag(adj_matrix %*% adj_matrix %*% adj_matrix)) / 2
print(num_closed_triangles)


# Parâmetro de heterogeneidade


deg <- degree(rede, mode="all")

hist(deg, breaks=seq(0, max(deg)+1, by=1), col="blue", xlab="Grau", ylab="Frequência", main="Distribuição de graus")
plot(deg, pch=20, col="blue", cex=2, xlab="Grau", ylab="Frequência", main="Distribuição de graus")


(ht <- mean(deg^2) / mean(deg)^2)



# Calcular a coreness para cada nó na rede
coreness_values <- coreness(rede)

# Encontrar o número total de conchas (shells) na rede
(num_conchas <- max(coreness_values))

# Contagem de nós em cada concha (shell)
for (i in 1:num_conchas) {
  dimensao_concha <- sum(coreness_values == i)
  print(paste("Número de nós na concha", i, ":", dimensao_concha))
}

plot(rede, vertex.size=5, vertex.label=NA, edge.arrow.size=0.5, 
     edge.curved=0.2, edge.color="gray", vertex.color="blue", vertex.frame.color="white", 
     vertex.label.color="black", layout=layout.fruchterman.reingold, main="Rede")

############################## 2 ########################################


# determinação da componente gigante

componentes <- components(rede)
maior_componente <- which.max(componentes$csize)
(componente_gigante <- induced.subgraph(rede, which(componentes$membership == maior_componente)))
plot(componente_gigante)

# dimensao da componente gigante

(dimensao_componente <- vcount(componente_gigante))

# numero de ligacoes da componente gigante

(ligacoes_componente <- ecount(componente_gigante))

# densidade da componente gigante

graph.density(componente_gigante)

# grau medio da componente gigante

mean(degree(componente_gigante))

# distribuicao de graus da componente gigante

degree_distribution(componente_gigante)


# Estudo da associação de grau da componente gigante

assortativity_degree(componente_gigante)

# media caminhos mais curtos da componente gigante

mean_distance(componente_gigante)

log(10, vcount(componente_gigante))

# Desta forma, pode-se concluir que a distância média não é pequena,
# pois é bastante diferente do logaritmo do número de nós na rede.



# diametro da componente gigante

diameter(componente_gigante)

# A distrância média da componente gigante é moderada à semelhança da rede




# Estudo e caracterização da existência de triângulos na rede


transitivity(componente_gigante, type = "global")

# Obter a matriz de adjacência
adj_matrix <- as.matrix(get.adjacency(componente_gigante))

# Calcular o número de triângulos fechados

(num_closed_triangles <- sum(diag(adj_matrix %*% adj_matrix %*% adj_matrix)) / 2)


# Parâmetro de heterogeneidade

graus <- degree(componente_gigante)
(heterogeneidade <- var(graus) / mean(graus)^2)

deg <- degree(componente_gigante, mode="all")

hist(deg, breaks=seq(0, max(deg)+1, by=1), col="blue", xlab="Grau", ylab="Frequência", main="Distribuição de graus")
plot(deg, pch=20, col="blue", cex=2, xlab="Grau", ylab="Frequência", main="Distribuição de graus")


(ht <- mean(deg^2) / mean(deg)^2)



## ???
graus <- degree(componente_gigante)

# Obter a média e o desvio padrão dos graus
media_graus <- mean(graus)
desvio_padrao_graus <- sd(graus)

# Calcular o coeficiente de variação
coeficiente_variacao <- desvio_padrao_graus / media_graus
print(coeficiente_variacao)


# Calcular a coreness para cada nó na rede
coreness_values <- coreness(componente_gigante)

# Encontrar o número total de conchas (shells) na rede
(num_conchas <- max(coreness_values))

# Contagem de nós em cada concha (shell)
for (i in 1:num_conchas) {
  dimensao_concha <- sum(coreness_values == i)
  print(paste("Número de nós na concha", i, ":", dimensao_concha))
}


plot(componente_gigante, vertex.size=5, vertex.label=NA, edge.arrow.size=0.5, 
     edge.curved=0.2, edge.color="gray", vertex.color="blue", vertex.frame.color="white", 
     vertex.label.color="black", layout=layout.fruchterman.reingold, main="Componente Gigante")





