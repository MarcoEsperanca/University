library(igraph)
library(ggplot2)

rede <- read_graph("trab_links.txt", format = c("edgelist"), directed=F)
# Salvar o gráfico em um arquivo SVG

plot(rede, vertex.size = 7, vertex.label.cex = .35)



# dimensao da rede

# vertices
vcount(rede)

# arestas
ecount(rede)

# densidade
edge_density(rede, loops = FALSE)

# grau medio
mean(degree(rede))


# distribuicao de graus

round(degree_distribution(rede),2)

# do a ggplot barplot of degree distribution with the values above each bar

library(ggplot2)

degree_dist <- round(degree_distribution(rede), 2)

# Cria um data frame com os graus e suas proporções
(degree_df <- data.frame(Grau = 0:(length(degree_dist)-1), Proporcao = degree_dist))



# Cria o gráfico de barras com a distribuição de grau na rede
ggplot(degree_df, aes(x = factor(Grau), y = Proporcao)) +
  geom_bar(stat = "identity", fill = "orange") +
  geom_text(aes(label = Proporcao), vjust = -0.5, size = 3) +
  labs(x = "Grau", y = "Proporção", title = "Distribuição de Grau na Rede") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))

ggsave("Imagens/distribuicao_grau_rede.svg")



# verificação se a rede é conexa
# caso não seja indica-se o tamanho mínimo e máximo da componente conexa

(is_connected <- is.connected(rede))
print(is_connected)

# identificação do do número de componentes, tamanho mínimo e máximo da componente conexa
if (!is_connected) {
  
  num_components <- length(components(rede))
  print(paste("Número de componentes:", num_components))
  
  component_sizes <- sizes(components(rede))
  min_size <- min(component_sizes)
  max_size <- max(component_sizes)
  print(paste("Tamanho mínimo da componente conexa:", min_size))
  print(paste("Tamanho máximo da componente conexa:", max_size))
}

# associação de grau

assortativity_degree(rede)

# diametro

diameter(rede)

# média dos caminhos mais curtos (distânci média)
mean_distance(rede)


# logaritmo para averiguar se a distância média é pequena
log10(vcount(rede))

# Desta forma, pode-se concluir que a distância média não é pequena,
# pois é bastante diferente do logaritmo do número de nós na rede.





# Uma distância média de 7.91 pode ser considerada moderada, 
# enquanto um diâmetro de 21 indica que há um par de nós na rede que está relativamente mais distante, 
# mas em geral, a rede possui uma média de distância moderada entre os nós.

# Esses valores podem variar dependendo do tamanho da rede e da natureza dos contatos sociais, 
# mas sugerem que, em média, os habitantes na zona residencial estão relativamente próximos uns dos outros, 
# enquanto ainda há uma certa distância entre os pares mais distantes.


# estudo da existência de triângulos na rede

# coeficiente de clustering da rede
transitivity(rede, type = "global")


# calcula o número de triângulos fechados
(numero_triangulos_rede <- sum(count_triangles(rede)))




# Parâmetro de heterogeneidade


deg <- degree(rede, mode="all")
(ht <- mean(deg^2) / mean(deg)^2)



# calcular a coreness para cada nó na rede
coreness_values <- coreness(rede)

# encontrar o número total de conchas (shells) na rede
(num_conchas <- max(coreness_values))

# contagem de nós em cada concha (shell)
for (i in 1:num_conchas) {
  dimensao_concha <- sum(coreness_values == i)
  print(paste("Número de nós na concha", i, ":", dimensao_concha))
}

# gráfico de barras com a distribuição de conchas na rede

ggplot(data.frame(coreness_values), aes(x = coreness_values)) +
  geom_bar(stat = "count", fill = "orange") +
  geom_text(stat = "count", aes(label = ..count..), vjust = -0.5, size = 3) +
  labs(x = "Concha", y = "Número de nós", title = "Distribuição de Conchas na Rede") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
  scale_x_continuous(breaks = 1:num_conchas)
ggsave("Imagens/distribuicao_conchas_rede.svg") # guardar gráfico num svg

# percentagem de nos em cada concha

for (i in 1:num_conchas) {
  dimensao_concha <- sum(coreness_values == i)
  print(paste("Percentagem de nós na concha", i, ":", (dimensao_concha / vcount(rede)) * 100))
}


data <- data.frame(
  concha = 1:num_conchas,
  percentagem = NA
)

for (i in 1:num_conchas) {
  data$percentagem[i] <- round((sum(coreness_values == i) / vcount(rede)) * 100, 2)
}

# excluir as conchas com 0% de nós
data_filtered <- subset(data, percentagem != 0)

# gráfico circular com a percentagem de nós em cada concha
ggplot(data = data_filtered, aes(x = "", y = percentagem, fill = factor(concha))) +
  geom_bar(stat = "identity", width = 1, color = "white") +
  coord_polar("y", start = 0) +
  labs(title = "Percentagem de nós em cada concha", fill = "Concha") +
  theme_void() +
  theme(legend.position = "right") +
  geom_text(aes(label = paste0(round(percentagem,1), "%")), position = position_stack(vjust = 0.5), angle = 60)
ggsave("Imagens/percentagem_conchas_rede.svg") # guardar gráfico num svg











plot(rede, vertex.size=5, vertex.label=NA, edge.arrow.size=0.5, 
     edge.curved=0.2, edge.color="gray", vertex.color="blue", vertex.frame.color="white", 
     vertex.label.color="black", layout=layout.fruchterman.reingold, main="Rede")

############################## 2 ########################################


# determinação da componente gigante

componentes <- components(rede)
maior_componente <- which.max(componentes$csize)
(componente_gigante <- induced.subgraph(rede, which(componentes$membership == maior_componente)))
plot(componente_gigante, vertex.size = 7, vertex.label.cex = .35)


# dimensao da componente gigante

(dimensao_componente <- vcount(componente_gigante))

# numero de ligacoes da componente gigante

(ligacoes_componente <- ecount(componente_gigante))

# densidade da componente gigante
edge_density(componente_gigante, loops = FALSE)



# grau medio da componente gigante

mean(degree(componente_gigante))

# distribuicao de graus da componente gigante
(degree_dist_cg <- round(degree_distribution(componente_gigante), 2))

# cria um data frame com os graus e suas proporções
(degree_df_cg <- data.frame(Grau = 0:(length(degree_dist_cg)-1), Proporcao = degree_dist_cg))


# gráfico de barras com a distribuição de graus na componente gigante
ggplot(degree_df_cg, aes(x = factor(Grau), y = Proporcao)) +
  geom_bar(stat = "identity", fill = "orange") +
  geom_text(aes(label = Proporcao), vjust = -0.5, size = 3) +
  labs(x = "Grau", y = "Proporção", title = "Distribuição de Grau na Componente Gigante") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))

ggsave("Imagens/distribuicao_grau_componente_gigante.svg") # guardar o gráfico num svg


# Estudo da associação de grau da componente gigante

assortativity_degree(componente_gigante)

# media caminhos mais curtos da componente gigante
mean_distance(componente_gigante)

# logaritmo para averiguar se a distância média é pequena
log10(vcount(componente_gigante))

# Desta forma, pode-se concluir que a distância média não é pequena,
# pois é bastante diferente do logaritmo do número de nós na rede.



# diametro da componente gigante

diameter(componente_gigante)

# A distrância média da componente gigante é moderada à semelhança da rede

# Distância grande




# Estudo e caracterização da existência de triângulos na rede


# coeficiente de clustering da rede
transitivity(componente_gigante, type = "global")


# calcula o número de triângulos fechados
(numero_triangulos_cg <- sum(count_triangles(componente_gigante)))

# calcula a percentagem do número de triângulos da compononente gigante 
# em relação ao número de triângulos da rede
(percentagem_triangulos_cg <- round((numero_triangulos_cg / numero_triangulos_rede) * 100, 1))

# Parâmetro de heterogeneidade



deg_cg <- degree(componente_gigante, mode="all")

hist(deg_cg, breaks=seq(0, max(deg_cg)+1, by=1), col="blue", xlab="Grau", ylab="Frequência", main="Distribuição de graus")
plot(deg_cg, pch=20, col="blue", cex=2, xlab="Grau", ylab="Frequência", main="Distribuição de graus")


(ht_cg <- mean(deg_cg^2) / mean(deg_cg)^2)



## ???
graus <- degree(componente_gigante)

# Obter a média e o desvio padrão dos graus
media_graus <- mean(graus)
desvio_padrao_graus <- sd(graus)

# Calcular o coeficiente de variação
coeficiente_variacao <- desvio_padrao_graus / media_graus
print(coeficiente_variacao)


# calcular a coreness para cada nó na rede
coreness_values <- coreness(componente_gigante)

# encontrar o número total de conchas (shells) na rede
(num_conchas <- max(coreness_values))

# contagem de nós em cada concha (shell)
for (i in 1:num_conchas) {
  dimensao_concha <- sum(coreness_values == i)
  print(paste("Número de nós na concha", i, ":", dimensao_concha))
}

ggplot(data.frame(coreness_values), aes(x = coreness_values)) +
  geom_bar(stat = "count", fill = "orange") +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.5, size = 3) +
  labs(x = "Concha", y = "Número de nós", title = "Distribuição de Conchas na Componente Gigante") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
  scale_x_continuous(breaks = 1:num_conchas)
ggsave("Imagens/distribuicao_conchas_componente_gigante.svg")

for (i in 1:num_conchas) {
  dimensao_concha <- sum(coreness_values == i)
  print(paste("Percentagem de nós na concha", i, ":", (dimensao_concha / vcount(componente_gigante)) * 100))
}


data_cg <- data.frame(
  concha = 1:num_conchas,
  percentagem = NA
)

for (i in 1:num_conchas) {
  data_cg$percentagem[i] <- round((sum(coreness_values == i) / vcount(componente_gigante)) * 100, 2)
}

# grafico circular com as percentagens como legenda


# excluir as conchas com 0% de nós
data_filtered_cg <- subset(data_cg, percentagem != 0)

# gráfico circular com a percentagem de nós em cada concha
ggplot(data = data_filtered_cg, aes(x = "", y = percentagem, fill = factor(concha))) +
  geom_bar(stat = "identity", width = 1, color = "white") +
  coord_polar("y", start = 0) +
  labs(title = "Percentagem de nós em cada concha na Componente Gigante", fill = "Concha") +
  theme_void() +
  theme(legend.position = "right") +
  geom_text(aes(label = paste0(round(percentagem,1), "%")), position = position_stack(vjust = 0.5), angle = 60)
ggsave("Imagens/percentagem_conchas_componente_gigante.svg")


