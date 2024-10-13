#import "template.typ": *
#include "capa.typ"
#show link: underline
#set math.equation(numbering: none)
// #set datetime.display(pattern: "[day]/[month]/[year]")
#import "@preview/tablex:0.0.5": gridx, tablex, rowspanx, colspanx, vlinex, hlinex
#show: project
#set page(numbering: "1 / 25")
#page(numbering:none)[
  #outline()
  // #outline(target: figure)
]
#pagebreak()
#counter(page).update(1)

= Introdução e _Business Understanding_ 

Entre 2012 e 2019, observou-se um aumento significativo no número de acidentes de viação com vítimas em Portugal Continental. Durante esse período, o total de acidentes passou de 29.867 para 35.704#footnote[https://www.pordata.pt/portugal/acidentes+de+viacao+com+vitimas+total+e+por+tipo+de+acidente+++continente-3093] e, falando em termos relativos, enquanto em 2012 o número de desastres com feridos ou mortos correspondia a $3 permille$ por mil habitantes, em 2020 este valor atingiu $3.6 permille$ #footnote[https://www.pordata.pt/portugal/acidentes+de+viacao+com+vitimas+por+mil+habitantes+++continente-1990], isto só em Portugal Continental. Este valor só decresceu em 2020 devido ao Covid-19. Infelizmente, o número de acidentes tem estado continuadamente a aumentar para os níveis pré-covid, aumentando 0.6 pontos permilhares em apenas 3 anos.

As rotundas têm um papel fundamental na circulação de viaturas, sendo uma interseção (giratória) #footnote[https://www.imt-ip.pt/sites/IMTT/Portugues/Planeamento/DocumentosdeReferencia/Planeamento-Acessibilidades-Gestao-Viaria/Documents/06Rotundas_AF.pdf] muito complexa devido ao seu excesso de regras que intensificam a segurança dos condutores na cirulação desta. Um exemplo dessas medidas, é a necessária redução de velocidades #footnote[https://doi.org/10.21307/tp-2020-013] <artigoRots>. Portugal possui 4851 rotundas, sendo o segundo país do mundo com maior número de rotundas _per capita_ #footnote[https://www.publico.pt/2023/11/02/local/noticia/portugal-nao-arrebata-titulo-capital-rotundas-perto-2068796]. Esta curiosidade inspirou-nos a realizar uma análise detalhada sobre as rotundas de Portugal, com especial atenção às suas relações com acidentes. Para resultados mais interessantes, optou-se por dar um maior foco à cidade de Viseu, cidade conhecida como "Cidade das Rotundas", sendo considerada como uma referência europeia relativamente ao planeamento urbano e à construção de infraestruturas, de acordo com o Departamento de Engenharia Civil (DEC) #footnote[https://dep.estgv.ipv.pt/departamentos/dcivil/viseu/]. O objetivo aqui é encontrar padrões entre as rotundas e visualizar potenciais características não visualizadas anteriormente sobre os acidentes. Para isso, nós: 

1. Examinamos acidentes em algumas rotundas de Viseu anedoticamente, de forma a investigar potenciais problemas que elas possam ter para a segurança dos condutores, passageiros e peões;

2. Usamos técnicas de aprendizagem não supervisionada de agrupamento de dados, de forma a explorar padrões consistentes e regras de associação entre os vários acidentes rodoviários em rotundas de Viseu, e analisamos os resultados perante eles próprios e o resto de Portugal (Continental).


#figure(
  image("Imagens/viseuRotundas.jpg", width: 70%),
  caption: [
    As Rotundas do concelho de Viseu
  ],
)
// #pagebreak() TODO FREITAS VE LA SE E SUPOSTO OU NAO TERPAGE BREAK AQUI DE ACORDO COM O PROF FALA OCOM O PLANHA TEEHEEHHEHEHEHE

// A realização deste trabalho tem como base dados fornecidos pela Autoridade Nacional de Segurança Rodoviária (ANSR), que forneceu um conjunto de acidentes rodoviários reportados em Portugal Continental entre 2010 e 2019. // A importância deste estudo reme (falta acabar)

/* Relativamente ao tema, optámos por focar na cidade de Viseu, uma cidade situada no coração de Portugal, conhecida pelas suas características únicas e pela grande densidade de rotundas na região, que a consolidaram como a "Cidade das Rotundas". Esta peculiaridade despertou-nos a curiosidade, levantando questões sobre o papel das rotundas no trânsito rodoviário e a incidência de acidentes associados a estes elementos urbanos, pela má fama associada aos portugueses ao circular em rotundas.

Ao longo deste trabalho, tentar-se-á procurar formas de responder a todas estas questões, mas para facilitar a rota de pensamento, as 2 questões foco escolhidas, serão:


- _*Primeira Questão:*_
*Serão as rotundas o epicentro de acidentes rodoviários? Em que medida a presença abundante desses elementos afeta a incidência de acidentes em uma cidade? E se tivermos como foco a tal "Cidade das Rotundas"?*

- _*Segunda Questão:*_
*Será possível identificar padrões distintos nos diversos acidentes rodoviários ocorridos em rotundas, de modo a categorizá-los em _clusters_ (grupos) específicos?*

Ao responder a essas perguntas, esperamos não apenas entender os fatores que contribuem para os acidentes em rotundas, mas também fornecer _insights_ valiosos para aprimorar a segurança rodoviária e a mobilidade urbana em Viseu e, talvez, suprimir mais o número de acidentes ocorridos no futuro.
*/


= _Data Understanding_

Antes de prosseguir para a manipulação e tratamento dos dados, é necessário compreender como os dados se encontram organizados. Estes foram fornecidos pela Autoridade Nacional de Segurança Rodoviária (ANSR), que forneceu todos os acidentes de viaturas que foram reportados às entidades fiscalizadores (PSP e GNR) em Portugal Continental entre 2010 e 2019.

Esses dados foram fornecidos em formato *.xlsx*, totalizando 10 ficheiros diferentes (acidentes do ano 2010 até 2019). É importante referir que estes possuem uma peculariedade, isto é, cada um dos ficheiros possui 4 _sheets_, representando uma perspetiva diferente dos acidentes. Estes 4 _sheets_ são os seguintes: `30 Dias_Cond_Veic`, `30 Dias_Passagm`, `30 Dias_Acidentes`, `30 Dias_Peões`. Apesar dos nomes já serem autoexplicativos, é notório que todos possuem `30 Dias`  referido no nome e isso faz com que seja necessário ter cuidado com a interpretação destes, pois é importante ter em conta que um acidente pode ocorrer num determinado dia, mas só é sinalizado e registado 10 dias depois. #footnote[Para melhor entendimento das variáveis originais, preenchidas no relatório http://www.ansr.pt/Estatisticas/BEAV/Documents/MANUAL%20PREENCHIMENTO%20BEAV.pdf]

// Para uma análise mais detalhadas de cada uma das variáveis, em anexo estarão todas as variáveis de cada um dos _sheets_ explicadas. (Colocar Link para os anexos) DEFINITAVAMENTE JÁ N VAMOS FAZER ISSO


Comecemos por visualizar os acidentes das rotundas em cada um dos distritos. A @porDistrito apresenta o número de acidentes absoluto e relativo a outro tipo de interseções, por distrito.

#figure(
  grid(
    columns: 2,
      image("Imagens/acidentesRotundasAbsoluto.svg"),
      image("Imagens/acidentesRotundasRelativo.svg"), 
  ),
  caption:[Número de acidentes de rotundas, absoluto e relativo a outras interseções]
) <porDistrito>

De acordo com o gráfico à esquerda, Lisboa tem o maior número de acidentes registados, seguido do Porto. Podemos assumir que isto acontece por estes tratarem-se de distritos com um elevado número de residentes comparado com o resto dos distritos. De acordo com o gráfico da direita, Viseu contem o maior número relativo de acidentes de rotundas, ainda que grande parte de acidentes não sejam em rotundas, com um máximo apenas de $approx 8%$. Podemos notar que Lisboa, mesmo que tenha o maior número de acidentes de rotundas, estas são uma minoria no distrito.

Na @heatmap podemos visualizar um _heatmap_ com todos os acidentes entre 2010 e 2019 do concelho de Viseu, com algumas rotundas circuladas. Podemos observar a grande densidade de rotundas no concelho, em conjunto de uma grande densidade de acidentes nelas.

#figure(
  image("Imagens/HeatMap.png", width: 100%),
  caption: [
    Heatmap com Acidentes em Viseu com rotundas assinaladas
  ],
) <heatmap>


Com este conhecimento, sentimo-nos confortáveis avançar com o nosso primeiro objetivo de investigar algumas rotundas de Viseu e as suas características. Optámos por analisar rotundas com alto número de feridos Graves ou mortos, ou baseado na sua localização geográfica, ou por alguma outra característica. As rotundas escolhidas estão notadas nas Figuras #ref(<5rotNferidos>, supplement: none) e #ref(<5rotNaturaza>, supplement: none), e as razões de análise serão ditadas nos seus respetivos capítulos.

A @5rotNferidos apresenta a quantidade de feridos que houve em cada uma das rotundas escolhidas durante os anos que temos acesso. Na @5rotNaturaza estão destacadas a natureza de cada um dos acidentes, com a respetiva quantidade.

// rotunda manhoso tem 1 morto
// praca republica e por tar no centro de iseu
// paulo sexto mais acidentes e alguns graves
// joao paulo II fica espersa da cidade so que e gigante
// carlos lopes e pq e gigante e tem muitas vias


// #figure(
//   table(
//   columns: 2,
//   stroke: 1pt,
//   inset: 10pt,
//   align: center,
//   [*Nome da Rotunda*], [*Número de Acidentes na Base de dados*], 
//   [Praça Paulo VI], [24],
//   [Praça João Paulo II], [24],
//   [Praça Carlos Lopes], [23],
//   [Rotunda Manhosa], [18],
//   [Praça República], [14]
// ), caption: [Rotundas com maior número de acidentes]
// ) 

#figure(
  image("Imagens/rotundasInteressantes.svg", width: 97%),
  caption: [
    Barras empilhadas com o número de acidentes em cada rotunda, organizados pela gravidade
  ],
) <5rotNferidos>

#figure(
  image("Imagens/top5RotundasOqaconteceu.svg", width: 100%),
  caption: [
    A natureza de cada um dos acidentes que ocorreram nas rotundas
  ],
) <5rotNaturaza>


Podemos observar que a maioria das rotundas  escolhidas têm um alto número de feridos, e que a rotunda Manhosa é das únicas que tem mortos. Podemos observar também que a Praça da República é a única entre as escolhidas que tem atropelamento de peões. 
Nos seguintes capítulos serão comentadas as características que distinguem estas rotundas das não escolhidas, como também serão mostradas imagens via satélite das mesmas para um reconhecimento e análise mais profundo das rotundas. Estando marcadas as localizações exatas dos acidentes fornecidas pela ANSR, é importante notar que nem todos os acidentes possuem as localizações certas na base de dados, especialmente para acidentes antes de 2013, onde uma grande parte de acidentes fiscalizados pela PSP não têm registo da sua localização exata. Portanto, nas imagens abaixo, o número de acidentes representados poderá não corresponder com os números referidos nas figuras anteriores.


== Rotunda Manhosa
A ideia de estudar esta rotunda surgiu do facto de esta registar bastantes acidentes e de ser situada num local de alta passagem de veículos, mas também porque teve um morto registado.

#figure(
  image("Imagens/rotundaManhosaEarth.png", width: 49%),
  caption: [
    Rotunda Manhosa
  ],
)


Esta rotunda possui 2 vias e 4 saídas. Ao lado encontra-se o Palácio de Gelo, um centro comercial, e portanto podemos pressupor que existe um elevado tráfego nesta rotunda.

#figure(
  grid(
    columns: 2,
    image("Imagens/rotundaManhosaMorto.png", width: 90%),
    image("Imagens/localMortoManhoso.png", width: 100%),
  ),
  caption: [
    Rotunda Manhosa
  ],
)

Esta é a única rotunda do concelho de Viseu, da base de dados, que apresenta um acidente onde houve uma vítima mortal. 

Após uma breve pesquisa, conseguimos descobrir que esta morte foi em 2011 de um jovem de 19 anos, de acordo com o Correio Da Manhã #footnote[https://www.cmjornal.pt/portugal/detalhe/morre-a-levar-pizza-pedida-pelo-irmao] . //Plancha - isto n parece etico, sedo a responsabilidade
Estaríamos a ser de certa forma injustos se disséssemos que esta rotunda é conhecida por causar a perda de uma vida, dado que foi apenas uma rara exceção entre 10 anos. No entanto, apesar deste caso específico, é importante salientar que os acidentes em rotundas raramente estão associados a grandes velocidades quer pela velocidade permitida pela lei, quer pela geografia usual destes locais #footnote[<artigoRots>].

== Praça Carlos Lopes

Esta rotunda fica situada na região Noroeste da cidade de Viseu e é registada como uma das rotundas mais perigosas dado o seu comprimento e o elevado número de saídas e vias. Esta rotunda tem o seu nome dedicado ao atleta Carlos Lopes #footnote[https://neotopografia.projectopatrimonio.com/obra/o-maratonista/].

#figure(
  grid(
    columns: 2,
    image("Imagens/pracaCarlosLopesEarth.png", width: 98%),
    image("Imagens/pracaCarlosLopesAcidentes.png", width: 98%),
  ),
  caption: [
    Praça Carlos Lopes
  ],
) <CarlosLopes>

Pela imagem acima, é notório que a rotunda pode ser complicada para novos condutores, devido às características referidas anteriormente; // Plancha - Quais ??????????????????????????????????????????
mesmo assim, ela não possui nenhum acidente grave, nem originou uma vítima mortal nesta base de dados. A rotunda continua a ter acidentes com inúmeros feridos ainda em 2023 #footnote[Exemplo: https://www.diarioviseu.pt/noticia/107281], potencialmente demonstrando que medidas ainda não foram tomadas nesta rotunda.
Atualmente, continuam a haver inúmeros acidentes nesta rotunda, sendo alguns exemplos deles:
#link("https://www.jornaldocentro.pt/noticias/diario/viseu-acidente-na-rotunda-carlos-lopes-fez-um-ferido-leve")[Exemplo1], #link("https://www.diarioviseu.pt/noticia/107281")[Exemplo2]. Também é importante referir que nela existe uma bomba de abastecimento de combustível e é possível observar que houve um despiste à saída dela. Conseguimos visualizar também que a maioria dos acidentes foram colisões laterais nas saidas à rotunda. Tendo em conta a imperfeição dos dados, podemos concluir que a forma da rotunda, em conjunto com a bomba com saída direta para a rotunda, contribui para uma maior probabilidade de vítimas na rotunda.

== Rotunda Paulo VI

A rotunda Paulo VI é a que apresenta maior número de feridos totais e de feridos graves na nossa base de dados.

#figure(
  grid(
    columns: 2,
      image("Imagens/PauloVIEarth.png", width: 100%),
      image("Imagens/PauloVIAcidentes.png", width: 89%),
  ),
  caption: [
    Rotunda Paulo VI
  ],
)<PauloVI>

Podemos notar a partir da @PauloVI que a rotunda é desproporcionalmente maior do que a maioria das rotundas no distrito. Ao lado da rotunda enncontra-se um McDonald's e o Instituto da Mobilidade e dos Transportes (IMT) de Viseu, o que pode indicar um número de peões acima do normal e justificar o número de feridos. Podemos notar também um caso de 3 feridos graves em um acidente apenas, algo extremamente raro na nossa base de dados.

== Praça da República

A Praça da República é uma rotunda localizada no centro de Viseu, com um número de atropelamentos acima da média de outros locais da cidade.

#figure(
  grid(
    columns: 2,
      image("Imagens/PracaRepublicaEarth.png", width: 60%),
      image("Imagens/PracaRepublicaAcidentes.png", width: 90%),
  ),
  caption: [
    Praça da República
  ],
) <PracaRepublica>

A @PracaRepublica demonstra a proximidade entre a rotunda e a respetiva praça que lhe dá o nome. Esta proximidade faz com que os acidentes ocorridos ao redor da rotunda sejam mais diversificados em comparação com outras áreas, como se pode observar na @TiposPracaRepublica. Dada a sua localização central na cidade, próxima a edifícios e frequentada por pedestres, é comum que ocorram mais atropelamentos de peões, tendo em conta a sua área geográfica.

#figure(
  image("Imagens/pracaRepublicaOqAconteceu.png", width: 80%),
  caption: [
    Tipos de acidentes na Praça da República
  ],
) <TiposPracaRepublica>

== Rotunda João Paulo II

Esta rotunda demonstra o maior índice de acidentes ligeiros, mas também uma grande dimensão com 3 vias de circulação na mesma. Talvez a razão seja por se situar numa zona de indústria perto de lojas em que as pessoas normalmente vão de carro.

#figure(
  grid(
    columns: 2,
      image("Imagens/JoaoPauloIIEarth.png", width: 99%),
      image("Imagens/JoaoPauloIIAcidentes.png", width: 98%),
  ),
  caption: [
    Rotunda Joao Paulo II
  ],
)

\
\
\
\

== Comparação evolutiva anual dos acidentes nas rotundas selecionadas

#figure(
  grid(
    columns: 1,
    image("Imagens/evolTop5Rotundas_acumulado.svg", width: 100%)
  ),
  caption: [
    Evolução do número de acidentes acumulativa anualmente
  ],
) <5rotEvolucao>

Para concluir a nossa investigação anedótica, na @5rotEvolucao é possível visualizar a evolução de número de acidentes acumulativa anual de cada uma das rotundas selecionadas. As conclusões que podemos tirar desta figura são as seguintes:

// TODO re analisar dps de mudar para cumolativo (Freitas)
- As Praças Paulo VI, João Paulo II e Carlos Lopes apresentam evoluções muito rápidas de acidentes, sendo estas as praças com o maior número de acidentes; a Praça João Paulo II é aquela que apresentou mais acidentes em 2010;
- A Praça da República não apresentou acidentes antes de 2013 e em 2018;
- A rotunda Manhosa sempre apresentou um crescimento lento do número de acidentes, menos em 2019, onde ocorreu um elevado crescimento;
- Em anexo, na @FiguraAcidentesdasRotundas, é possível visualizar o número de acidentes que ocorreram em cada um dos anos, de forma individual.

= _Data Preparation_

O nosso objetivo será fazer agrupamento de acidentes de rotundas de forma a encontrar padrões. Para esse fim, decidimos filtrar para estas rotundas. Usámos como critério se a rotunda contém no nome "rotunda", ou se for identificada como tal pelas entidades fiscalizadoras, independentemente das latitudes e longitudes marcadas. A @Filtragem mostra dois exemplos destes acidentes.

#figure(
  grid(
    columns: 2,
      image("Imagens/naoRotundanaRotunda.png", width: 55%),
      image("Imagens/tipoRotundaForaRotunda.png", width: 64%),
  ),
  caption: [
    Filtragem dos dados
  ],
  
) <Filtragem>


== Transformação e Seleção dos Dados
A presente secção detalha as transformações e preparações efetuadas nos conjuntos de dados deste projeto, de forma a simplificar interpretabilidade futura, ambos para resultados melhores e para analisá-los facilmente. A @expVars apresenta um resumo das variáveis selecionadas. 

#figure(
  table(
    columns: (auto, auto),
    inset: 10pt,
    align: horizon,
    [*Variável*], [*Significado*],
    [`oqueaconteceu_geral`], [Motivo do acidente (colisão / despiste / atropelamento)],
    [`condAtmosferica`], [Condições climatérias],
    [`luminosidade`], [Período do dia e respetiva luminosidade],
    [`n_feridos`], [Número de feridos total],
    [`faixa etaria condutores`], [Faixa etária dos condutores dividida em: < 29, 30-59 e > 60],
    [`havia_passageiros`], [Verifica se havia passageiros no acidente],
    [`DiaSemana`], [Dia da semana do acidente],
    [`sin_percentage_year`], [_*Sin*_ da conversão da data do ano em segundos para radianos],
    [`cos_percentage_year`], [_*Cos*_ da conversão da data do ano em segundos para radianos],
    [`sin_seconds`], [_*Sin*_ da conversão das horas do dia em segundos para radianos],
    [`cos_seconds`], [_*Cos*_ da conversão das horas do dia em segundos para radianos],
    [`condEstradaLumped`], [Condições do pavimento da estrada],
    [`isCapital`], [Variável para ver se o acidente foi numa capital de distrito] 
),
caption: [Explicação das variáveis selecionadas para o _clustering_]
) <expVars>

Algumas das variáveis na tabela encontram-se sem transformações, enquanto que outras sofreram de tal. Essas outras são as seguintes:

- `oqueaconteceu_geral`: Dado o registo de vários tipos de acidentes que poderiam pertencer ao mesmo grupo, foram agregados tipos de acidentes de modo a ficar com três classes: Despites, Colisões e Atropelamentos. Os Atropelamentos, apesar de representarem uma minoria na base de dados (cerca de 4%), foram introduzidos porque são sempre casos possíveis de ocorrer em rotundas;
- `n_feridos`: Representa qual foi a quantidade de feridos que o acidente provocou, num valor inteiro. Se existiu um ferido grave e um leve no mesmo acidente o valor desta variável é 2;
- `faixa etaria condutores`: Foram agrupados os condutores por um intervalo de idades, de forma a distingui-los entre pessoas mais jovens e idosas. Para isso, foi feita uma separação conforme demonstrado na @GEtariosep. Daí foi retirado que o grupo etário fosse separado em 3 grupos, por < 29, 30-59, > 60;

- `havia_passageiros`: Representa se nos carros envolvidos no acidente existiam passageiros, em valor booleano. Ou seja, se hipoteticamente um acidente envolve 2 carros e apenas os condutores estão nos carros, esta variável tem o valor de FALSE;
- `sin_percentage_year`/`cos_percentage_year`/`sin_seconds`/`cos_seconds`: Está explicado mais detalhadamente na @capConvTemp;
- `condEstradaLumped`: Identifica se um acidente ocorreu com boas condições de estrada (Seco e Limpo) ou em Outras circunstâncias, que inclui também más condições destas;
- `isCapital`: Leva em conta o nome da freguesia e do distrito e identifica se o nome da freguesia representa uma capital de distrito. Foi realizada esta tranformação para tentar diferenciar acidentes que acontecem em zonas rurais ou urbanas, visto que a área, a quantidade e o tráfico de estradas e rotundas nas capitais de distrito é maior do que em zonas menos povoadas, no restante do distrito. Se o acidente ocorreu na freguesia de Viseu, por exemplo, esta variável tem o valor TRUE. 

#figure(
  image("Imagens/grupo_etario.png", width: 85%),
  caption: [
    Alteração das Horas
  ],
)<GEtariosep>

/*
- *Agrupamento de Grupos Etários*: Os grupos etários foram unificados para facilitar a análise por faixa etária.
- *Ano de Matrícula*: Transformamos anos de matrícula anteriores a 1900 em "NA" para garantir a integridade dos dados.
- *Criação de novas variáveis*: Foram incluídas colunas para indicar se foi realizado teste de álcool, se o veículo era especial, se havia deficiência no pneu, se o veículo possuía seguro, assim como uma variável para saber se o local de acidente se encontrava em uma capital.
- *Identificação por ID*: Cada condutor, passageiro e peão recebeu uma identificação única para fins de referência (idCondutor, idPassageiro, idPeao).
- *Condição da Estrada Simplificada*: A condição da estrada foi categorizada em "Seco e Limpo" ou outras condições.
- *Filtragem por Localização e Tipo de Acidente*: Selecionamos apenas acidentes ocorridos em rotundas, explicitamente mencionados ou presentes no nome do local do acidente.
- *Generalização dos Tipos de Acidente e Idades dos Condutores*: Categorizamos os tipos de acidente como "despiste", "colisão" ou "atropelamento" e agrupamos as idades dos condutores nas seguintes faixas etárias: < 29, 30-59 e > 60.
- *Cálculo de Feridos*: Determinamos o número total de feridos ligeiros e graves considerando peões, passageiros e condutores envolvidos.
*/

== Conversão do tempo <capConvTemp>

Na elaboração das nossas transformações e seleção de variáveis, chegamos a um problema sobre de como codificar a altura do ano e a altura do dia. Podíamos ter simplesmente colocado os dias/segundos decorridos, mas o problema seria que não informa o nosso modelo que as variáveis são cíclicas, ou seja, acidentes que ocorreram no fim do dia/ano teriam uma grande distância de acidentes que ocorreram no início do dia/ano seguinte, mesmo se a distância delas fosse mínima. Por exemplo:

#let date = datetime(
  year:2022,
  month:12,
  day:30
)
#let sum = duration(
  days:3
)

#let summed = date + sum

$ 
"00:15AM" &=> 900 "segundos occorido em um dia" \
"11:30PM" &=> 84600 "segundos occorido em um dia" \
// mais facil por casuse dos anos bisestos
date.display("[day]/[month]/[year]") &=> date.ordinal() "dias ocorridos no ano" \
summed.display("[day]/[month]/[year]") &=> summed.ordinal() "dias ocorridos no ano"
$

Se codificássemos como apresentado, o modelo iria classificar que estes acidentes teriam uma grande distância, sendo que $84600 >> 900$ e $364 >> 2$; no entanto, a distância entre eles é de #((30+15)*60) segundos e 3 dias.

Para resolvermos este problema, decidimos codicicar de forma cíclica #footnote[Com base neste _blog_: https://ianlondon.github.io/blog/encoding-cyclical-features-24hour-time/].

Visualizemos a conversão abaixo:

$ "HH:MM" => "segundos passados em um dia" * (2pi) /  (24h dot 60min dot 60sec) $
$ "00:15AM": 900 dot (2pi) / (24 dot 60 dot 60) = pi/48 $
$ "11:30PM": 84600 dot (2pi) / (24 dot 60 dot 60) = (47pi)/24 $

#set rect(
  inset: 28pt,
  fill: rgb("dcdcdc"),
  width: 60%,
  stroke: 1pt,
)

#figure(
  grid(
    columns: 2, gutter: -1pt,
    rows: 1,
    rect([
      
Na imagem ao lado, podemos visualizar os valorses dos horários, referidos anteriormente, convertidos em ângulos. Por último, bastará então calcular o seno e o cosseno dos respetivos ângulos obtidos.

*00:15AM*

$ sin(pi/48) approx 0.06540313$

$ cos(pi/48) approx 0.9978589$

*11:30PM*

$sin((47pi)/24) approx -0.1305262$

$cos((47pi)/24) approx 0.9914449$

], width: 100%),
    image("Imagens/trigExemplo.svg", width: 100%)
  ),
  caption: [
    Trigonometria das horas
  ],
)

Comparando agora os resultados, é notório que estes se encontram mais próximos que anteriormente, demonstrando assim que o objetivo de colocar o valor dos segundos cíclico foi alcançado.


//#figure(
//  image("Imagens/SinCosHoras.svg", width: 70%),
//  caption: [
//    Transformação das Horas dos acidentes das rotundas de Viseu
//  ],
//)

// === Conversão da época do ano

// O problema que há com as horas diárias, também existe com o respetivo dia do acidente. Dando um breve exemplo, a distância entre 31 de Dezembro com o dia 1 de Janeiro é pequena, tendo a distância de um único dia, mas como fazemos o modelo entender isso?
// Para chegar a uma solução, também foi usada a trigonometria, tal e qual o ponto anterior, mas agora com breves diferenças. Primeiramente foi calculado a percentagem, que aquele dia representa quando comparado com o ano inteiro. Para uma compreensão mais fácil, de seguida será demonstrado um exemplo com os respetivos passos:

// - 1º: Identificar a data:
//   - *15/07/2017*
// - 2º: Do primeiro dia do respetivo ano da data anterior, 01/01/2017, até à data do acidente passaram quantos segundos?
//   - 17 971 200 segundos
// - 3º: Identificar quantos segundos tem o ano (ter em conta se é um ano bissexto ou não):
//   - 31 556 926 segundos
// - 4º: Calcular a persentagem:
//   - $(17971200)/(31556926) approx 0.5694851$

// Tendo já calculado a respetiva persentagem, basta agora multiplicar por $2pi$ e, de seguida, calcular o respetivo $sin$ e $cos$. Abaixo podemos então visualizar os resultados obtidos:

// $ sin(2pi dot 0.5694851) approx -0.4228498 $
// $ cos(2pi dot 0.5694851) approx -0.9061998 $

#align(horizon)[
  #figure(
  grid(
    columns: 2,
      image("Imagens/trigAno.svg", width: 100%),
      
      image("Imagens/SinCosHoras.svg", width: 100%),
  ),
  caption: [
    Filtragem dos dados
  ],
  
)
]


//#figure(
  //image("Imagens/trigAno.svg", width: 67%),
//  caption: [
  //  Trigonometria no dia do ano
//  ],
//)

// No gráfico acima, podemos visualizar todas as datas dos acidentes da base de dados com a respetiva conversão realizada no exemplo anterior. Para finalizar o exemplo, visualizando o resultado obtido, é possivel visualizar que, realmente, o ponto se encontra localizado no grupo *julho*.
// Este gráfico não aparenta ser tão enriquecedor como o do horário do dia, pois, os pontos encontram-se bem uniformes ao longo dos anos, mas poderá ser útil na criação dos modelos.

= Análise dos resultados do _clustering_

De seguida, procedeu-se à técnica de agrupamento (_clustering_) de variáveis. 
Em primeiro lugar, usámos métodos de _clustering_ hierárquicos, de forma a identificar um número adequado de grupos (_clusters_), para usar um método baseado em centroides. Para ajudar na decisão, também foi usado o método da silhueta #footnote[https://doi.org/10.1016/0377-0427(87)90125-7], que se resume a aplicar o algoritmo para vários números de clusters e verificar aquele que apresenta maior valor de silhueta.
De seguida, executamos o algoritmo para os acidentes das rotundas de Viseu, e analisamos os resultados. Finalmente, aplicamos o algoritmo com os centroides anteriormente calculados para o resto das rotundas de Portugal Continental, de forma a investigar se os mesmos padrões podem ser extrapolados para o resto do País.

Como função de distância, usámos a distância de Gower #footnote[Usando a função `daisy` do pacote `cluster` https://www.rdocumentation.org/packages/cluster/versions/2.1.6/topics/daisy], uma métrica de similaridade adequada para tipos de dados numéricos, ordinais e nominais. 

Como método de _clustering_, decidimos usar o algoritmo de Partição Sobre Medoides (PSM/PAM), um algoritmo similar a _k-means_ mas que usa os medoides invés, nomeado por Rousseeuw #footnote[https://doi.org/10.1002/9780470316801.ch2]. 

Decidimos usar este invés de outros métodos, pois este algoritmo torna-se mais relevante quando usamos distâncias mais complexas, como a distância de Gower. 
Após a análise dos resultados do _clusterings_ hierárquicos e do método da silhoueta #footnote[Este encontra-se no #ref(<silhueta>, supplement: "Anexo")], decidimos usar como número de clusters $k = 4$.

Além disso, de forma a podermos obter informações adicionais sobre o acidente, utilizamos a variável `GNR_PSP` como variável de _PROFILE_, uma vez que através da área de atuação de cada uma: `GNR` (rural) e `PSP` (urbana) #footnote[https://www.msn.com/pt-pt/noticias/other/qual-a-diferen%C3%A7a-de-fun%C3%A7%C3%B5es-da-gnr-e-da-psp/ar-AA18RylF], podemos inferir se o acidente ocorreu numa área rural ou urbana, oferecendo _insights_ adicionais sobre a caracterização do acidente e a sua alocação no _cluster_.
Também utilizámos a `latitude` e a `longitude` como variáveis de _PROFILE_ para ver a localização dos acidentes atribuídos a cada _cluster_ no mapa.


== Análise no concelho de Viseu

Para a caracterização dos _clusters_ iremos utilizar a tabela seguinte, com base no que foi mencionado acima.

#figure(
   table(
    columns: (auto, auto, auto),
    inset: 10pt,
    align: horizon,
    [*Nº _cluster_*], [*`GNR`*], [*`PSP`*],
    [1], [65], [93],
    [2], [31], [142],
    [3], [141], [42],
    [4], [102], [233]
  ),
    caption: [Alocação de cada acidente para cada _cluster_ numa zona rural (`GNR`) ou urbana (`PSP`) em Viseu]
)

// TODO juntar perfil

Através deste último algoritmo, relembrado que foi o que apresentou melhores resultados, atribuímos cada uma dessas observações a um dos 4 _clusters_. As conclusões que pudemos retirar da criação dos _clusters_ e a sua respetiva alocação de observações foram as seguintes:

#pagebreak()

=== _Cluster_ 1 <Cluster1Viseu>

#figure(
  image("Imagens/cluster_1.svg", width: 100%),
  caption: [
    Resultados para o _cluster_ 1
  ],
)

#figure(
  image("Imagens/cluster_1_viseu_altura_ano.svg", width: 100%),
  caption: [
    Evolução dos acidentes do _cluster_ 1 ao longo do ano
  ],
)


*Condições climatéricas adversas*: A partir das variáveis `condAtmosferica_Chuva` e `condEstradaLumped_Other` observa-se que as condições climatéricas adversas têm um elevado foco neste _cluster_ de acidentes, sendo importante comentar sobre a chuva, assim como a existência de condições desfavoráveis ao piso nas estradas, fazendo-nos assumir que, provavelmente, os acidentes deste _cluster_ possuiam o piso escorregadio, o que propicia o aumento do número de acidentes. Além disso, no segundo gráfico, sugere-se que, neste _cluster_, a maioria dos acidentes ocorreram no outono/inverno, o que está de acordo com a designação que decidimos atribuir a este _cluster_.

#pagebreak()

=== _Cluster_ 2 <Cluster2Viseu>


#figure(
  image("Imagens/cluster_2.svg", width: 100%),
  caption: [
    Resultados para o _cluster_ 2
  ],
)

#figure(
  image("Imagens/cluster_2_viseu_altura_dia.svg", width: 100%),
  caption: [
    Evolução dos acidentes do _cluster_ 1 ao longo do dia
  ],
)

*Condutores jovens/adultos em saídas noturnas*: Suportado pelas variáveis `luminosidade_Noite,com iluminação`,`Condutores < 29` e  `Condutores 30-59` e `havia_passeiros`: constata-se uma predominância de acidentes em período noturno em condutores jovens/adultos, com um elevado número de passageiros, ocorrendo essencialmente em zonas urbanas. Desta forma, este _cluster_ pode representar as saídas à noite de jovens com os seus amigos. A ideia de que a maioria dos acidentes se registou no período noturno, pode ser reforçada pelo segundo gráfico, que possui uma maior concentração dos pontos no lado direito do gráfico, que representam horários noturnos.

#pagebreak()

=== _Cluster_ 3 <Cluster3Viseu>

#figure(
  image("Imagens/cluster_3.svg", width: 100%),
  caption: [
    Resultados para o _cluster_ 3
  ],
)

#figure(
  image("Imagens/cluster_3_viseu_altura_dia.svg", width: 100%),
  caption: [
    Evolução dos acidentes do _cluster_ 3 ao longo do dia
  ],
)



#figure(
  image("Imagens/cluster_3_viseu_altura_ano.svg", width: 100%),
  caption: [
    Evolução dos acidentes do _cluster_ 3 ao longo do ano
  ],
)



*Despistes de condutores idosos*: Baseado na variável `oqaconteceu_geral_Despiste`, verifica-se que a maioria dos acidentes são despistes provocados por condutores idosos (`Condutores > 60`) e em zonas rurais que também costumam ser caracterizadas por uma população mais envelhecida, podendo estar associados a um menor tempo de reação destes e, consequentemente, estarem mais propícios a acidentes. Além disso, pelos segundo e terceiro gráficos, é possível constatar que a maioria dos acidentes parece ocorrer na primavera/verão durante o período da manhã. (Ambos os gráficos apresentam uma maior concentração dos pontos no lado esquerdo)

#pagebreak()

=== _Cluster_ 4 <Cluster4Viseu>

#figure(
  image("Imagens/cluster_4.svg", width: 100%),
  caption: [
    Resultados para o _cluster_ 4
  ],
)

\

#figure(
  image("Imagens/cluster_4_viseu_altura_dia.svg", width: 100%),
  caption: [
    Evolução dos acidentes do _cluster_ 4 ao longo do dia
  ],
)

*Colisões*: Através da variável `oqaconteceu_geral_Colisão`, neste _cluster_ encontram-se predominantemente as colisões com condições atmoféricas normais, ocorrendo na sua maioria em zonas urbanas. O segundo gráfico parece sugerir que a maioria das colisões ocorreram no período de deslocação casa-trabalho e vice-versa, o que, se analisado corretamente, apresenta alguma lógica, pois, quando as pessoas estão a ir para o trabalho ou a voltar para casa costumam estar mais apressadas e cansadas.

#pagebreak()

=== Acidentes com latitude e longitude de perfil

Passemos agora para a caracterização dos _clusters_ através da perfilagem das coordenadas geográficas dos acidentes. (Relembramos que nem todos os acidentes estão representados, uma vez que alguns deles não possuíam coordenadas)


#figure(
  image("Imagens/clusters_viseu_maps_labeled.jpg", width: 100%),
  caption: [
    Mapa com a alocação de cada uma das observações nos respetivos _clusters_ e a sua localização no mapa
  ],
)



No mapa apresentado, verifica-se a existência de poucos acidentes assinalados a azul, uma vez que a maioria dos acidentes no concelho de Viseu são registados em zonas urbanas. Relativamente aos acidentes atribuídos com a cor violeta, existem de forma abundante, estando espalhados pelo concelho inteiro. Os acidentes assinalados a verde correspondem a acidentes ocorridos predominantemente à noite, tal como veremos de seguida, tendo uma maior concentração em zonas centrais (urbanas). Os sinistros a laranja representam condições adversas, quer meteorológicas, quer das condições da estrada.

/*- Azul nao existe tanto pq n rural 
- Violeta é colisões muitos sitios
- Verde mais à noite como veremos em seguida
- Laranja chuva e condições da estrada como veremos em seguida */

#align(horizon)[
  #figure(
  grid(
    columns: 2,
    rows: 1,
    image("Imagens/carlos_lopes_galp.png", width: 88%, height: 25%),
    image("Imagens/carlos_lopes_laranja.png", width: 70%),
  ),
  caption: [
    _Clustering_ na Praça Carlos Lopes
  ],
)<acidentemaps>
]


O local representado nas duas imagens desta figura representa uma zona urbana na Praça Carlos Lopes, sugestão essa reforçada pela ausência de acidentes assinalados a azul, que costumam ser característicos das zonas rurais, pela variável de perfil `GNR_PSP` já estudada.

Na imagem à direita é possível verificar a existência de acidentes representados a verde que identificam tipicamente os acidentes noturnos, enquanto os assinalados a roxo representam locais em que, normalmente, o tipo de acidentes mais comuns são colisões, sendo representados pelos _clusters_ 2 e 4, respetivamente.

Por fim, os acidentes asssinados a laranja possuem uma peculiaridade. De acordo com a cobertura de carro do _Google Maps_, constata-se que em 2009 não havia nenhum sinal de _stop_, enquanto nos mapas de 2014 e 2018 estava colocado um sinal de _stop_ tal como ilustrado na imagem à esquerda de julho de 2018 (pequeno poste preto a dizer _stop_). É possível que as pessoas não tivessem reparado no sinal tal como mostra o acidente de 2015 na @acidentemaps. O sinal foi substituído algures entre 2018 e 2019, sendo que dos sinistros que têm latitude e longitude foram registados no _cluster_ 1 (laranja). Por todas estas razões, a estrada podia estar em más condições naquele período, que é impossível de visualizar no _Google Maps_ porque só tem datas espaçadas.


// - representa uma zona urbana (n ha azuis)
// - os verdes sao a noite e os roxos são colisões que são caracterizados como acidentes "mais comuns"
// - laranja de acordo com a cobertura do carro do Google Maps, é um sítio que em 2009 n tinha nenhum sinal de stop e em 2014 e 2018 tinha um sinal de stop como o da figura de julho 2018 (pequeno poste preto a dizer stop); talvez as pessoas não reparassem no sinal e é o q mostra o acidente de 2015 na figura; o sinal foi substituido algures entre 2018 e 2019... dos que têm lat e long foi caracterizado no _cluster_ 1 (laranja) por estas razoes mas pq a estrada podia estar em más condiçoes naquele periodo que é impossivel de ver no Google Maps porque so tem datas espaçadas

\

== Análise em Portugal inteiro e comparação com o cenário anterior

Passaremos agora a analisar o cenário em todo o Portugal Continental e comparar com o cenário anterior.
Abaixo apresenta-se a alocação da zona do acidente (rural ou urbana) em cada _cluster_:

#figure(
   table(
    columns: (auto, auto, auto),
    inset: 10pt,
    align: horizon,
    [*Nº _cluster_*], [*`GNR`*], [*`PSP`*],
    [1], [1029], [1681],
    [2], [928], [1278],
    [3], [2081], [3076],
    [4], [1502], [2332]
  ),
  caption: [Alocação de cada acidente para cada cluster numa zona rural (`GNR`) ou urbana (`PSP`) para Portugal Continental]
)

#pagebreak()

=== _Cluster_ 1

#figure(
  image("Imagens/cluster_1_portugal.svg", width: 80%),
  caption: [
    Resultados para o _cluster_ 1
  ],
)

*Despistes à noite*: Neste _cluster_ à semelhança do _cluster_ 2 do cenário anterior (@Cluster2Viseu), os acidentes verificam-se predominantemente à noite, mas não há predominância dos mesmos em condutores jovens e verificando-se essencialmente despistes. Estes ocorrem, maioritariamente, em zonas urbanas, zonas essas que são as que costumam ter mais tráfego à noite, comparativamente às zonas rurais.

=== _Cluster_ 2

#figure(
  image("Imagens/cluster_2_portugal.svg", width: 80%),
  caption: [
    Resultados para o _cluster_ 2
  ],
)

*Condições atmosféricas adversas*: Semelhante ao _cluster_ 1 do cenário anterior (@Cluster1Viseu) este é caracterizado por acidentes em condições atmosféricas adversas e nos mesmas estações do ano (outono/inverno).

#pagebreak()

=== _Cluster_ 3

#figure(
  image("Imagens/cluster_3_portugal.svg", width: 80%),
  caption: [
    Resultados para o _cluster_ 3
  ],
)

#figure(
  image("Imagens/cluster_3_portugal_altura_ano.svg", width: 80%),
  caption: [
    Evolução dos acidentes do _cluster_ 3 ao longo do ano
  ],
)


*Colisões*: Semelhante ao _cluster_ 4 do cenário anterior (@Cluster4Viseu) onde se apresentam maioritariamente colisões, registados em zonas urbanas. A maioria destas registam-se na primavera/verão tal como sugere o segundo gráfico.

#pagebreak()

=== _Cluster_ 4

#figure(
  image("Imagens/cluster_4_portugal.svg", width: 80%),
  caption: [
    Resultados para o _cluster_ 4
  ],
)

\

#figure(
  image("Imagens/cluster_4_portugal_altura_ano.svg", width: 80%),
  caption: [
    Evolução dos acidentes do _cluster_ 4 ao longo do ano
  ],
)


*Colisões de condutores idosos*: Relativamente análogo ao _cluster_ 3, a maioria dos acidentes são provocados por condutores idosos, mas neste cenário a maior parte dos acidentes são colisões e não despistes como no anterior (@Cluster3Viseu) , contudo, registam-se mais acidentes nas zonas urbanas. Além disso, de acordo com o segundo gráfico, estes acidentes não parecem ocorrer durante a época do verão.

// TODO: ANALISAR ESTE GRAFICO ABAIXO E TALVEZ COMPARAR VISEU COM LISBOA E COIMBRA, POR EXEMPLO (IDEIA DO PLANCHA E QUE O BOTAS ACHA VÁLIDA)

#figure(
  image("Imagens/clusters_portugal3.svg", width: 53%),
  caption: [
    Alocações das observações por cada _cluster_ no mapa de Portugal Continental
  ],
)

O gráfico acima demonstra que existe uma maior concentração dos acidentes nas rotundas no litoral, causada pela litoralização,  sendo uma exceção o alentejo litoral #footnote[https://www.dn.pt/sociedade/desequilibrio-na-distribuicao-populacional-pelo-territorio-acentuou-se-15380510.html]. Comentando sobre os _clusters_ obtidos em Portugal e em Viseu, os grupos obtidos em cada um destes são bastante parecidos, dando assim a entender que Viseu não apresenta acidentes "únicos" nas rotundas, ou seja, os problemas que existem em Viseu, relativamente às rotundas, são, de grosso modo, muito parecidos com os problemas das rotundas em Portugal Continental, dando assim a entender que os resultados obtidos não foram muito enriquecedores para a descoberta de características chave em Viseu. É importante ter em conta que esta conclusão está limitada aos dados que foram fornecidos, que são uma mera amostra de todos os acidentes que ocorrem em Portugal.

#pagebreak()

= Conclusão

Feita a análise dos acidentes nas rotundas no concelho de Viseu, é evidente que os _insights_ obtidos desempenham um papel vital na compreensão da dinâmica acidental na região. Os resultados significativos que emergiram podem ser úteis para a compreensão extensa dos acidentes de rotundas não só de Viseu, mas também do resto dos distritos de Portugal Continental, e das diferenças entre eles.

Segundo o Automóvel Clube de Portugal (ACP), vários acidentes ocorrem devido a comportamentos de risco na estrada#footnote[https://www.acp.pt/veiculos/condutor-em-dia/conduzir-em-seguranca/12-comportamentos-de-risco-na-estrada]. A falta de civismo e o desrespeito pela regras rodoviárias impactam de forma significativa o número de acidentes. Uma prática bastante comum em rotundas é a saída repentina do centro da rotundas, muitas vezes sem a devida e atempada sinalização, podendo apanhar vários condutores desprevinos. Esta situação ainda se torna mais perigosa quando o condutor conduz de forma descuidada e/ou em situações de pouca visibilidade, como à noite #footnote[exemplo de acidente: https://www.cmjornal.pt/portugal/detalhe/motociclista-ferido-em-colisao-com-carro-em-viseu] e em dias que existam situações climatéricas adversas (como, por exemplo, o nevoeiro).

Existem várias medidas já pré-estabelecidas para controlar e proteger todos os condutores, tendo como exemplo os limites de velocidade #footnote[https://www.bomcondutor.pt/biblioteca/resumo-velocidades] que, pelas rotundas se localizarem dentro de localidades, limitam a circulação nestas a uma velocidade máxima de 50 km/h; mesmo assim, é referido no código da estrada #footnote[https://www.invicta.pt/pdf/legislacao/Codigo%20da%20Estrada%202014.pdf]
pelo #underline("Artigo 25.º Velocidade moderada") que nas rotundas "... o condutor deve moderar especialmente a velocidade". Somado a este controlo de velocidade, também existem regras de como se deve circular numa rotunda, estando sujeito a coima #footnote[https://www.bomcondutor.pt/biblioteca/resumo-circulacao-rotundas] todos os indivíduos que desrespeitarem as regras. Em conjunto com isto, a Autarquia de Viseu procurou diminuir o número de acidentes com a instalação de semáforos limitadores de velocidade a 50 Km/h em 2017 #footnote[https://www.cmjornal.pt/portugal/cidades/detalhe/radares-e-semaforos-na-circular-de-viseu]. A PSP realizou recentemente a campanha "Viajar sem pressa" #footnote[https://www.jornaldocentro.pt/noticias/diario/psp-viseu-2023-com-mais-viaturas-controladas-e-menos-multas] na Rotunda João Paulo II (a rotunda com maior número de feridos @5rotNferidos em Viseu). Estes factos demonstram que medidas já estão a ser tomadas para aumentar a segurança na estrada e reduzir o número de acidentes.

 Segundo as próprias autoridades: “Se um veículo circular a 30 km/h, a probabilidade das consequências de um atropelamento serem mortais é de 10%. Aumentando a velocidade para 50 km/h, a probabilidade passa a ser de 80%”, logo fica assim subentendido que este controlo de velocidades é fundamental para uma circulação segura. 

Mesmo assim, estas medidas não são o suficiente para dar resposta aos acidentes, como é possivel visualizar na @FiguraAcidentes que mostra todos os acidentes que ocorreram nas rotundas de Viseu, sendo notório que não houve um decréscimo constante.

Em suma, para enfrentar os desafios persistentes relacionados aos acidentes em rotundas, é imperativo adotar uma abordagem abrangente e multifacetada. A implementação de campanhas educativas, a intensificação da fiscalização, melhorias na sinalização e iluminação são passos cruciais na promoção da segurança rodoviária. Uma solução poderia ser a implementação das *Turbo-rotundas* #footnote[https://pplware.sapo.pt/motores/turbo-rotundas-como-funcionam/] (#link("https://core.ac.uk/download/pdf/70644343.pdf")[Documento sobre a Turbo-Rotunda]), método que apresentou resultados incríveis relativamente à diminuição de acidentes, podendo usar como exemplo os Países Baixos que, após a implementação desta nova rotunda, os acidentes reduziram-se em 80%. 

Recomendamos que realizem futuros projetos e análises a fim de identificar possiveis problemas associados a outros distritos e/ou a outros tipos de intersecções, de forma a promover uma percepção realista dos acidentes de viaturas neste País; seja com outros métodos, outros dados, ou outras interpretações.

#figure(
  image("Imagens/TurboRotunda.jpg", width: 100%),
  caption: [Turbo Rotunda]
)

#pagebreak()
// #counter(page).update(n => 24)

= Anexos

== Anexo A - Possível caminho da vítima mortal na rotunda Manhosa

#figure(
  image("Imagens/caminho.png", width: 100%),
)

\

== Anexo B - Número de acidentes nas rotundas de Viseu por mês

#figure(
  image("Imagens/evolTop5Rotundas.svg", width: 100%),
) <FiguraAcidentesdasRotundas>

\

== Anexo C - Número de acidentes nas rotundas de Viseu por mês

#figure(
  image("Imagens/todosAcidentes.svg", width: 110%),
) <FiguraAcidentes>

== Anexo D - Método de Silhueta <silhueta>

#figure(
  image("Imagens/silhueta.jpg")
)

/*

== Anexo Z - Tabela com designação das variáveis

#gridx(
    columns: 9,
    rows: 90,
    header-rows: 2,
    align:(x, y) => {
      if (x == 0){return right}; //header
      if (y in (0, 1)) {return center};//row-names
      return right
    },
    /* --- header --- */
    [],colspanx(2)[Acidentes $arrow.b$], colspanx(2)[Peões $arrow.b$], colspanx(2)[Condutores $arrow.b$], colspanx(2)[Passageiros $arrow.b$], hline_header(start:1, end:3),hline_header(start:3, end:5),
    hline_header(start:5, end:7), hline_header(start:7, end:9),
    [],colspanx(2)[Original],colspanx(2)[Original],colspanx(2)[Original],colspanx(2)[Original],
    hline(start:1),
    /* -------------- */
    [id.Acidente], vline(start:2), colspanx(2)[A variavel representa um indetificador único dos acidentes],colspanx(2)[Tem],colspanx(2)[Yes],colspanx(2)[Tem],
    [Datahora], vline(start:2), colspanx(2)[Representa a data e a hora de um determinado acidente],colspanx(2)[Tem],colspanx(2)[Tem],colspanx(2)[Tem],
    [Dia], vline(start:2), colspanx(2)[Representa a variavel do dia],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Mês], vline(start:2), colspanx(2)[essa variável representa os meses],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Entidades Fiscalizadoras], vline(start:2), colspanx(2)[GNR (zonas rurais) ou PSP (zonas urbanas)],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Velocidade local], vline(start:2), colspanx(2)[Limite geral de velocidade da via onde ocorreu o acidente],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Velocidade geral], vline(start:2), colspanx(2)[Velocidade máxima permitida no local ],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Dia da Semana], vline(start:2), colspanx(2)[Dia da semana do acidente],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Latitude GPS], vline(start:2), colspanx(2)[Representa a coordenada da latitude],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Longitude GPS], vline(start:2), colspanx(2)[Representa a coordenada da longitude],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Num. Mortos a 30 dias], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Num. Feridos graves a 30 dias], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Num. Feridos ligeiros a 30 dias], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Características Tecnicas1], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Cond Aderência], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Distrito], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Concelho], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Freguesia], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Pov. Proxima], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Nome arruamento], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Tipos Vias], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Sexo], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Lesões a 30 dias], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Teste Alcool], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Acções Condutores], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Licença Condução], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Inf. Comp. a Acções e Manobras], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Acções Peão], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Acessórios Condutores], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[Acessórios Passageiro],colspanx(2)[],
    [Ano matricula], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Carga Lotação], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Categoria Veículos], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Certificado Adr], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Cod Via], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Condutor GR.Etario Sum], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Estado Conservação], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Factores atmosféricos], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Hora], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Id. Passageiro], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Id. Peão], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Inspeção periódica], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [inspeção Vias], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Km], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [localizações], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Luminosidade], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Marca via], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Natureza], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [nomeoutrosfatores], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [obras arte], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Obstáculos], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Pneus], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Posição veículo], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Reg Circulação1], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Seguros], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Sentidos], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Sinais], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Sinais Luminosos], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Tempo Condução Continuada], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Tipo Natureza], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Tipo Piso], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Tipo Serviço], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],  
    [Tipo Veículo], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Traçado 1], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Traçado 2], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Traçado 3], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Traçado 4], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [veículo especial], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [Via Trânsito], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    [], vline(start:2), colspanx(2)[],colspanx(2)[],colspanx(2)[],colspanx(2)[],
    
  )

*/



