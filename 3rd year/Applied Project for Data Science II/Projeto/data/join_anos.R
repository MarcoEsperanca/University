library(archive)

final_acidentes <- tibble()
final_condutores <- tibble()
final_passageiros <- tibble()
final_peoes <- tibble()

acidentes_types <- tribble(
  ~NomeColuna, ~Tipo,
  "idAcidente"           ,as.character,
  "datetime"             ,ymd_hms,
  "dia"                  ,\(x) NA_character_,
  "mês"                  ,\(x) NA_character_,
  "hora"                 ,\(x) NA_character_,
  "GNR_PSP"              ,\(x) ifelse(x == "Guarda Nacional Republicana", "GNR", "PSP"),
  "velocidadeLocal"      ,as.integer,
  "velocidadeGeral"      ,as.integer,
  "DiaSemana"            ,as_factor,
  "Latitude"             ,\(x) x %>% gsub(",", ".", .) %>% as.double(),
  "Longitude"            ,\(x) x %>% gsub(",", ".", .) %>% as.double(),
  "nMortos"              ,as.integer,
  "nFeridosGraves"       ,as.integer,
  "nFeridosLigeiros"     ,as.integer,
  "AutoEstrada_SemSep"   ,as_factor,
  "condEstrada"          ,as_factor,
  "distrito"             ,as_factor,
  "concelho"             ,as.character,
  "freguesia"            ,as.character,
  "povProxima"           ,as.character, # n sei o q e isto
  "nomeRua"              ,as.character,
  "tipoVia"              ,as_factor,
  "nomeVia"              ,as.character,
  "estadoEstrada"        ,as_factor,
  "kmDaEstrada"          ,as.double,
  "condAtmosferica"      ,as_factor,
  "sentido"              ,as_factor,
  "interseccao"          ,as_factor,
  "localOuNao"           ,as_factor,
  "luminosidade"         ,as_factor,
  "marcasRua"            ,as_factor,
  "oqaconteceu"          ,as_factor, # "nome pouco profissional" - Plancha
  "obraArte"             ,as_factor, # discutir sobre isto (n sei)
  "obstaculos"           ,as_factor,
  "sentidoAutoEstrada"   ,as_factor,
  "sinalizacao"          ,as_factor,
  "sinaisLuminosos"      ,as_factor,
  "tipoPiso"             ,as_factor,
  "recta_curva"          ,as_factor,
  "inclinacao"           ,as_factor,
  "bermasEstrada"        ,as_factor,
  "tipoPista"            ,as_factor, # ver melhor dps com outros nomes
  "via_transito"         ,as_factor
)

condutores_types <- tribble(
  ~NomeColuna, ~Tipo,
  "idAcidente"           ,as.character,
  "datetime"             ,\(x) NA_character_,
  "sexo"                 ,\(x) NA_character_,
  "lesaoCondutor"        ,as_factor,
  "licencaCarta"         ,as_factor,
  "testeAlcool"          ,as_factor,
  "acaoPreAcidente"      ,as_factor,
  "acao_infoComplementar",as_factor,
  "estado_condutor"      ,as_factor,
  "tempoConducao"        ,as_factor,
  "acessorioCondutor"    ,as_factor,
  "categoriaVeiculo"     ,as_factor,
  "tipoVeiculo"          ,as_factor,
  "tipoServico"          ,as_factor,
  "tipoVeiculoEspecial"  ,as_factor,
  "anoMatricula"         ,as.integer,
  "inspecao_veiculo"     ,as_factor,
  "certificadoADR"       ,as_factor,
  "cargaLevada"          ,as_factor,
  "estadoPneus"          ,as_factor,
  "seguroVeiculo"        ,as_factor,
  "distrito"             ,as_factor, # VER SE É NECESSÁRIO TIRAR 
  "concelho"             ,as.character, # VER SE É NECESSÁRIO TIRAR 
  "GE-Contudor_menosOu5"     ,as.logical,
  "GE-Contudor_entre6e9"     ,as.logical,
  "GE-Contudor_entre10e14"   ,as.logical,
  "GE-Contudor_entre15e17"   ,as.logical,
  "GE-Contudor_entre18e20"   ,as.logical,
  "GE-Contudor_entre21e24"   ,as.logical,
  "GE-Contudor_entre25e29"   ,as.logical,
  "GE-Contudor_entre30e34"   ,as.logical,
  "GE-Contudor_entre35e39"   ,as.logical,
  "GE-Contudor_entre40e44"   ,as.logical,
  "GE-Contudor_entre45e49"   ,as.logical,
  "GE-Contudor_entre50e54"   ,as.logical,
  "GE-Contudor_entre55e59"   ,as.logical,
  # n está no sample entre 60 e 64 PARA CONDUTOR APENAS (talvez seja aquilo de estar tudo a zero?)
  "GE-Condutor_entre65e69"   ,as.logical,
  "GE-Condutor_entre70e74"   ,as.logical,
  "GE-Condutor_maisOu75"     ,as.logical,
  "GE-Condutor_naoDef"       ,as.logical
  )

passageiros_types <- tribble(
  ~NomeColuna, ~Tipo,
  "idAcidente"                 ,as.character,
  "datetime"                   ,\(x) NA_character_,
  "GNR_PSP"                    ,\(x) ifelse(x == "Guarda Nacional Republicana", "GNR", "PSP"), # dps verif. !!!
  "idPassageiro"               ,as.integer,
  "lesaoPassageiro"            ,as.factor,
  "sexo"                       ,as_factor,
  "posicaoVeiculo"             ,as_factor,
  "acessorioPassageiro"        ,as_factor,
  "distrito"                   ,as_factor, # VER SE É NECESSÁRIO TIRAR 
  "concelho"                   ,as.character, # VER SE É NECESSÁRIO TIRAR
  "GE-Passageiro_menosOu5"     ,as.logical,
  "GE-Passageiro_entre6e9"     ,as.logical,
  "GE-Passageiro_entre10e14"   ,as.logical,
  "GE-Passageiro_entre15e17"   ,as.logical,
  "GE-Passageiro_entre18e20"   ,as.logical,
  "GE-Passageiro_entre21e24"   ,as.logical,
  "GE-Passageiro_entre25e29"   ,as.logical,
  "GE-Passageiro_entre30e34"   ,as.logical,
  "GE-Passageiro_entre35e39"   ,as.logical,
  "GE-Passageiro_entre40e44"   ,as.logical,
  "GE-Passageiro_entre45e49"   ,as.logical,
  "GE-Passageiro_entre50e54"   ,as.logical,
  "GE-Passageiro_entre55e59"   ,as.logical,
  "GE-Passageiro_entre60e64"   ,as.logical,
  "GE-Passageiro_entre65e69"   ,as.logical,
  "GE-Passageiro_entre70e74"   ,as.logical,
  "GE-Passageiro_maisOu75"     ,as.logical,
  "GE-Passageiro_naoDef"       ,as.logical
)

peoes_types <- tribble(
  ~NomeColuna, ~Tipo,
  "idAcidente"            ,as.character,
  "freguesia"             ,as_factor,
  "oqaconteceu"           ,as_factor,
  "oqaconteceu_especifico",as_factor,
  "datetime"              ,\(x) NA_character_,
  "GNR_PSP"               ,\(x) ifelse(x == "Guarda Nacional Republicana", "GNR", "PSP"), # dps verif. !!!
  "idPeao"                ,as.integer,
  "sexo"                  ,as_factor,
  "acaoPeao"              ,as_factor,
  "distrito"              ,as_factor, # VER SE É NECESSÁRIO TIRAR 
  "concelho"              ,as.character, # VER SE É NECESSÁRIO TIRAR
  "lesaoPeao"             ,as_factor,
  "GE-Peao_menosOu5"     ,as.logical,
  "GE-Peao_entre6e9"     ,as.logical,
  "GE-Peao_entre10e14"   ,as.logical,
  "GE-Peao_entre15e17"   ,as.logical,
  "GE-Peao_entre18e20"   ,as.logical,
  "GE-Peao_entre21e24"   ,as.logical,
  "GE-Peao_entre25e29"   ,as.logical,
  "GE-Peao_entre30e34"   ,as.logical,
  "GE-Peao_entre35e39"   ,as.logical,
  "GE-Peao_entre40e44"   ,as.logical,
  "GE-Peao_entre45e49"   ,as.logical,
  "GE-Peao_entre50e54"   ,as.logical,
  "GE-Peao_entre55e59"   ,as.logical,
  "GE-Peao_entre60e64"   ,as.logical,
  "GE-Peao_entre65e69"   ,as.logical,
  "GE-Peao_entre70e74"   ,as.logical,
  "GE-Peao_maisOu75"     ,as.logical,
  "GE-Peao_naoDef"       ,as.logical
)

for (ano in 2010:2019) {
  here("ANSR-acidentes", "dados", paste0("acidentes-", ano, ".xlsx")) -> path
  acidentes    <- readxl::read_excel(path, sheet = 3, skip = 1, col_names = acidentes_types$NomeColuna)
  condutores   <- readxl::read_excel(path, sheet = 1, skip = 1, col_names = condutores_types$NomeColuna)
  passageiros  <- readxl::read_excel(path, sheet = 2, skip = 1, col_names = passageiros_types$NomeColuna)
  peoes        <- readxl::read_excel(path, sheet = 4, skip = 1, col_names = peoes_types$NomeColuna)
  
  # transform every "NÃO DEFINIDO" em NA em todas as tabelas
  acidentes %<>% mutate_if(is.character, ~if_else(.x == "NÃO DEFINIDO", NA_character_, .x))
  condutores %<>% mutate_if(is.character, ~if_else(.x == "NÃO DEFINIDO", NA_character_, .x))
  passageiros %<>% mutate_if(is.character, ~if_else(.x == "NÃO DEFINIDO", NA_character_, .x))
  peoes %<>% mutate_if(is.character, ~if_else(.x == "NÃO DEFINIDO", NA_character_, .x))
  
  # for all columns
  for (col in names(acidentes)) {
    # apply the function in the types table
    acidentes[[col]] <- acidentes_types[acidentes_types$NomeColuna == col, "Tipo"][[1]][[1]](acidentes[[col]])
  }
  for (col in names(condutores)) {
    condutores[[col]] <- condutores_types[condutores_types$NomeColuna == col, "Tipo"][[1]][[1]](condutores[[col]])
  }
  for (col in names(passageiros)) {
    passageiros[[col]] <- passageiros_types[passageiros_types$NomeColuna == col, "Tipo"][[1]][[1]](passageiros[[col]])
  }
  for (col in names(peoes)) {
    peoes[[col]] <- peoes_types[peoes_types$NomeColuna == col, "Tipo"][[1]][[1]](peoes[[col]])
  }
  
  final_acidentes %<>% bind_rows(acidentes)
  final_condutores%<>% bind_rows(condutores)
  final_passageiros %<>% bind_rows(passageiros)
  final_peoes %<>% bind_rows(peoes)
}
if(!dir.exists(here("data", "original"))) {dir.create(here("data", "original"))}

final_acidentes   %>% janitor::remove_empty("cols") %>% arrow::write_parquet(here("data", "original", "acidentes.parquet"))
final_condutores  %>% janitor::remove_empty("cols") %>% arrow::write_parquet(here("data", "original", "condutores.parquet"))
final_passageiros %>% janitor::remove_empty("cols") %>% arrow::write_parquet(here("data", "original", "passageiros.parquet"))
final_peoes       %>% janitor::remove_empty("cols") %>% arrow::write_parquet(here("data", "original", "peoes.parquet"))

archive_write_dir(here("data", "original.7z"), here("data", "original"))

# delete dir
unlink(here("data", "original"), recursive = TRUE)

