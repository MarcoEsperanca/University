acidentes <- arrow::read_parquet(here("data", "nomes_marotos", "acidentes.parquet"))
condutores <- arrow::read_parquet(here("data", "nomes_marotos", "condutores.parquet"))
passageiros <- arrow::read_parquet(here("data", "nomes_marotos", "passageiros.parquet"))
peoes <- arrow::read_parquet(here("data", "nomes_marotos", "peoes.parquet"))

acidentes %<>% mutate(year = year(datetime))
condutores %<>% left_join(acidentes %>% select(idAcidente, year), by = "idAcidente")
passageiros %<>% left_join(acidentes %>% select(idAcidente, year), by = "idAcidente")
peoes %<>% left_join(acidentes %>% select(idAcidente, year), by = "idAcidente")

condutoresGE <- condutores %>% 
  mutate(n_idades = select(., starts_with("GE")) %>% rowSums()) %>% 
  mutate(`GE-Condutor_entre60e64` = if_else(n_idades == 0, T, F)) %>%
  # change where true to name of col if True
  mutate(grupo_etario = 
           fcase(
             `GE-Contudor_menosOu5`, "< 5",
             `GE-Contudor_entre6e9`, "6 - 9",
             `GE-Contudor_entre10e14`, "10 - 14",
             `GE-Contudor_entre15e17`, "15 - 17",
             `GE-Contudor_entre18e20`, "18 - 20",
             `GE-Contudor_entre21e24`, "21 - 24",
             `GE-Contudor_entre25e29`, "25 - 29",
             `GE-Contudor_entre30e34`, "30 - 34",
             `GE-Contudor_entre35e39`, "35 - 39",
             `GE-Contudor_entre40e44`, "40 - 44",
             `GE-Contudor_entre45e49`, "45 - 49",
             `GE-Contudor_entre50e54`, "50 - 54",
             `GE-Contudor_entre55e59`, "55 - 59",
             `GE-Condutor_entre60e64`, "60 - 64",
             `GE-Condutor_entre65e69`, "65 - 69",
             `GE-Condutor_entre70e74`, "70 - 74",
             `GE-Condutor_maisOu75`, "> 75",
             `GE-Condutor_naoDef`, NA_character_,
             default = NA_character_
           ) %>% factor(levels = c("< 5", "6 - 9", "10 - 14", "15 - 17", "18 - 20", "21 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59", "60 - 64", "65 - 69", "70 - 74", "> 75"))
  ) %>% 
  select(-n_idades, -starts_with("GE"))

passageiros %>% 
  mutate(n_idades = select(., starts_with("GE")) %>% rowSums()) %>% 
  mutate(`GE-Passageiro_entre60e64` = if_else(n_idades == 0, T, F)) %>%
  # change where true to name of col if True
  mutate(grupo_etario = 
           fcase(
             `GE-Passageiro_menosOu5`, "< 5",
             `GE-Passageiro_entre6e9`, "6 - 9",
             `GE-Passageiro_entre10e14`, "10 - 14",
             `GE-Passageiro_entre15e17`, "15 - 17",
             `GE-Passageiro_entre18e20`, "18 - 20",
             `GE-Passageiro_entre21e24`, "21 - 24",
             `GE-Passageiro_entre25e29`, "25 - 29",
             `GE-Passageiro_entre30e34`, "30 - 34",
             `GE-Passageiro_entre35e39`, "35 - 39",
             `GE-Passageiro_entre40e44`, "40 - 44",
             `GE-Passageiro_entre45e49`, "45 - 49",
             `GE-Passageiro_entre50e54`, "50 - 54",
             `GE-Passageiro_entre55e59`, "55 - 59",
             `GE-Passageiro_entre60e64`, "60 - 64",
             `GE-Passageiro_entre65e69`, "65 - 69",
             `GE-Passageiro_entre70e74`, "70 - 74",
             `GE-Passageiro_maisOu75`, "> 75",
             `GE-Passageiro_naoDef`, NA_character_,
             default = NA_character_
           ) %>% factor(levels = c("< 5", "6 - 9", "10 - 14", "15 - 17", "18 - 20", "21 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59", "60 - 64", "65 - 69", "70 - 74", "> 75"))
  ) %>%
  select(-n_idades, -starts_with("GE")) -> passageirosGE

peoes %>% 
  mutate(n_idades = select(., starts_with("GE")) %>% rowSums()) %>% 
  mutate(`GE-Peão_entre60e64` = if_else(n_idades == 0, T, F)) %>%
  # change where true to name of col if True
  mutate(grupo_etario = 
           fcase(
             `GE-Peao_menosOu5`, "< 5",
             `GE-Peao_entre6e9`, "6 - 9",
             `GE-Peao_entre10e14`, "10 - 14",
             `GE-Peao_entre15e17`, "15 - 17",
             `GE-Peao_entre18e20`, "18 - 20",
             `GE-Peao_entre21e24`, "21 - 24",
             `GE-Peao_entre25e29`, "25 - 29",
             `GE-Peao_entre30e34`, "30 - 34",
             `GE-Peao_entre35e39`, "35 - 39",
             `GE-Peao_entre40e44`, "40 - 44",
             `GE-Peao_entre45e49`, "45 - 49",
             `GE-Peao_entre50e54`, "50 - 54",
             `GE-Peao_entre55e59`, "55 - 59",
             `GE-Peao_entre60e64`, "60 - 64",
             `GE-Peao_entre65e69`, "65 - 69",
             `GE-Peao_entre70e74`, "70 - 74",
             `GE-Peao_maisOu75`, "> 75",
             `GE-Peao_naoDef`, NA_character_,
             default = NA_character_
           ) %>% factor(levels = c("< 5", "6 - 9", "10 - 14", "15 - 17", "18 - 20", "21 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59", "60 - 64", "65 - 69", "70 - 74", "> 75"))
  ) %>%
  select(-n_idades, -starts_with("GE")) -> peoesGE

condutoresF <- condutoresGE %>% 
  mutate(
    anoMatricula = ifelse(anoMatricula < 1900, NA_integer_, anoMatricula),
    lesaoCondutor = lesaoCondutor %>% fct_relevel("Ileso", "Ferido leve", "Ferido grave", "Morto"),
    # categoriaVeiculo tem desconhecido spearado de n definido
    feztesteAlcol   = if_else(testeAlcool %>% str_starts("Submetido"), T, F),
    eraEspecial     = if_else(is.na(tipoVeiculoEspecial), F, T),
    deficienciaPneu = if_else(estadoPneus %>% str_starts("Com"), T, F),
    tinhaSeguro     = if_else(seguroVeiculo %>% str_starts("Não"), F, T),
  ) %>% 
  group_by(idAcidente) %>% 
  mutate(idCondutor = row_number(idAcidente)) %>% 
  ungroup() %>% 
  relocate(idAcidente, idCondutor) %>%
  arrange(idCondutor) %>% arrange(idAcidente) %>% 
  select(-year)

acidentesF <- acidentes %>% 
  mutate(
    condEstradaLumped = condEstrada %>% fct_lump_n(1),
    GNR_PSP = GNR_PSP %>% as_factor(),
  ) %>% 
  select(-year)

passageirosF <- passageirosGE %>% 
  select(-GNR_PSP, -distrito, -concelho, -year) %>% 
  relocate(idAcidente, idPassageiro) %>%
  arrange(idPassageiro) %>% arrange(idAcidente) 

peoesF <- peoesGE %>% 
  group_by(idAcidente) %>% 
  mutate(idPeao = row_number(idAcidente)) %>%
  ungroup() %>%
  relocate(idAcidente, idPeao) %>%
  arrange(idPeao) %>% arrange(idAcidente) %>%
  select(-year, -GNR_PSP, -distrito, -concelho)

passageirosF %>% 
  select(idAcidente, idPassageiro) %>% 
  group_by(idAcidente) %>%
  summarise(nPassageiros = n()) -> nPassageiros
peoesF %>% 
  select(idAcidente, idPeao) %>% 
  group_by(idAcidente) %>%
  summarise(nPeoes = n()) -> nPeoes
condutoresF %>%
  select(idAcidente, idCondutor) %>% 
  group_by(idAcidente) %>%
  summarise(nVeiculos = n()) -> nVeiculos

acidentesFF <- acidentesF %>% 
  left_join(nPassageiros, by = "idAcidente") %>% 
  left_join(nPeoes, by = "idAcidente") %>% 
  left_join(nVeiculos, by = "idAcidente") %>% 
  mutate(
    nPassageiros = if_else(is.na(nPassageiros), 0, nPassageiros),
    nPeoes = if_else(is.na(nPeoes), 0, nPeoes),
    nVeiculos = if_else(is.na(nVeiculos), 0, nVeiculos),
  )

acidentesFiltradoWOLATLONG <- acidentesFF %>%
  # rotundas
  filter(
    (!is.na(interseccao) & interseccao == "Em rotunda") | 
      (!is.na(nomeRua) & nomeRua %>% str_to_lower() %>% str_detect("rotunda")) |
      # excecao para a praca Carlos lopes
      (distrito == "Viseu" & !is.na(nomeRua) & nomeRua %>% str_to_lower() %>% str_detect("carlos lopes"))
  ) %>%
  # viseu
  mutate(EmViseu = ifelse(distrito == "Viseu", T, F))

acidentesFiltradoWOLATLONG %>% 
  select(-kmDaEstrada, -sentidoAutoEstrada) %>%
  mutate(isCapital = distrito == concelho) -> acidentesFiltrado

write_parquets(
  "cleaned_all_lat_long",
  acidentesFiltrado, condutoresF, passageirosF, peoesF,
  substitute = FALSE
)
