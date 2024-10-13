# PACDII
TODO README, usa o `rig` (ou o conda) pra gerir instalações do R (ou o conda) (melhor conda )
## Criacao dos dados

1. Download dos dados
2. Extrair dentro do repositorio
3. Correr `data/join_anos.R`

Alternativamente os dados estao disponiveis nos `releases` no github (à direita). Faz download diretamente do que precisa ou usa o `gh release download`.

```
gh release download -D "data" -p "*.parquet"
```

Todos os archivos estão nos releases

```
gh release list

gh release download 01.12 -D "data" -p "*.7z"
gh release download 28.11 -D "data" -p "*.7z"
gh release download 21.11 -D "data" -p "*.7z"
gh release download 14.11 -D "data" -p "*.7z"

cd data\
7z x .\ -o.\*
```
se no linux ou max ent as barras sao ao contrario
