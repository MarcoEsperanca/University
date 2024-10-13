# Instale a biblioteca ggplot2 se ainda não estiver instalada
# install.packages("ggplot2")

# Carregue a biblioteca ggplot2
library(ggplot2)

# Defina os ângulos
angle1 <- (47 * pi) / 24
angle2 <- pi / 48
angle3 <- pi / 2
angle4 <- pi
angle5 <- 3 * pi / 2
angle6 <- 0

# Crie um dataframe com as coordenadas dos pontos do círculo
circle_points <- data.frame(
  x = cos(seq(0, 2 * pi, length.out = 100)),
  y = sin(seq(0, 2 * pi, length.out = 100))
)

# Crie um dataframe com as coordenadas dos pontos específicos
df <- data.frame(
  x = c(0, cos(angle1), cos(angle2), cos(angle3), cos(angle4), cos(angle5), cos(angle6)),
  y = c(0, sin(angle1), sin(angle2), sin(angle3), sin(angle4), sin(angle5), sin(angle6))
)

# Rótulos para serem adicionados manualmente
label_text <- c("0", expression((47 * pi) / 24), expression(pi / 48),
                expression(pi / 2), expression(pi), expression(3 * pi / 2))

# Crie o gráfico
trigExemplo <- ggplot() +
  geom_path(data = circle_points, aes(x, y), color = "darkblue", size = 1) +
  geom_point(data = df, aes(x, y), color = "red", size = 3) +
  annotate("text", x = c(cos(0) - .35, cos(angle1), cos(angle2), cos(angle3) - .1, cos(angle4) - .1, cos(angle5) - .1),
           y = c(0, sin(angle1), sin(angle2) + .1, sin(angle3) + .1, sin(angle4), sin(angle5) - .05),
           label = label_text, hjust = c(-10, 0, -.1, 0, 0, 0), size = 5) +
  geom_segment(data = df, aes(x = 0, y = 0, xend = x, yend = y), 
               linetype = "dashed", color = "black", size = 0.7) +
  geom_hline(yintercept = 0, linetype = "solid", color = "black", size = 0.7) +
  geom_vline(xintercept = 0, linetype = "solid", color = "black", size = 0.7) +
  coord_fixed(ratio = 1) +
  xlim(c(-1.5, 1.5)) +
  ylim(c(-1.5, 1.5)) +
  theme_minimal() +
  theme(
    axis.title = element_blank(),
  )

trigExemplo

ggsave("trigExemplo.svg", trigExemplo, width = 8, height = 8)
