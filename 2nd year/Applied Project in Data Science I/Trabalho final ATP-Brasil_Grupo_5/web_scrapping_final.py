import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import numpy as np

df_brasil = pd.read_csv('atpplayers_to_web_scrap.csv')

df_brasil['DateStart'] = pd.to_datetime(df_brasil['DateStart'])
df_brasil['DateEnd'] = pd.to_datetime(df_brasil['DateEnd'])



# Obtém uma lista de jogadores únicos
unique_players = df_brasil['LinkPlayer'].unique()

# Inicia uma sessão HTML para fazer solicitações na web
session = HTMLSession()


################################################################ RankPlayer #################################################################

print("Web scrapping RankPlayer ...\n")

# Itera sobre cada linha dos links únicos
for player in unique_players:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    
    # Itera sobre cada linha associada a este jogador
    for index, row in player_rows.iterrows():
        
        # Check if RankPlayer is NaN
        if pd.isnull(row['RankPlayer']):
            # Extract the year from the DateStart column
            year = pd.to_datetime(row['DateStart']).year
          
            # Extract the player's last name from the PlayerName column
            last_name = row['PlayerName'].split()[-1].lower()
            
            # URL
            url = f'https://www.tennisexplorer.com/player/{last_name}/?annual={year}/'
            print(url)
            
            response = session.get(url)
            # Extract the HTML
            html = response.html.html
            soup = BeautifulSoup(html, "html.parser")
            # Encontrar o elemento current/highest rank for singles
            rank_element = soup.find('div', text=re.compile('Current/Highest rank - singles'))
        #    print(rank_element.text)
            
            if rank_element:
                if 'Current/Highest rank - singles: -' in rank_element.text:      
                    rank_number = re.findall('\d+', rank_element.text)[0]
                    df_brasil.at[index, 'RankPlayer'] = int(rank_number)

                    
                elif 'Current/Highest rank - singles: -' not in rank_element.text:

                    # Extrair o número do elemento
                    rank_number = rank_element.text.split(':')[1].split('.')[0].strip()
   
                    # Atualizar a coluna RankPlayer do DataFrame
                    df_brasil.at[index, 'RankPlayer'] = int(rank_number)
                    
                #else:
                   # print("Bruh")
                   # rank_number = re.findall('\d+', rank_element.text)[0]
                   # print(rank_number)
   
            
            else:
                # Se o rank não é encontrado, mantém-se como NaN no DataFrame
                df_brasil.at[index, 'RankPlayer'] = np.nan
            

dicionario_jogadores_em_falta = {
    'Sebastian Baez': 'https://www.tennisexplorer.com/player/baez-a8fb1/',
    'Joao Menezes' : 'https://www.tennisexplorer.com/player/menezes-a5e18/',
    'Gilbert Klier Junior' : 'https://www.tennisexplorer.com/player/klier-junior-75c19/',
    'Martin Cuevas' : 'https://www.tennisexplorer.com/player/cuevas-de8b1/',    
    'Christian Lindell' : 'https://www.tennisexplorer.com/player/lindell-7e33a/',
    'Wilson Leite' : 'https://www.tennisexplorer.com/player/leite-f2563/',
    'Rafael Matos' : 'https://www.tennisexplorer.com/player/matos-33d92/',
    'Matias Soto' : 'https://www.tennisexplorer.com/player/soto-fec8d/',
    'Joao Souza' : 'https://www.tennisexplorer.com/player/souza-fe947/',
    'Gabriel Roveri Sidney' : 'https://www.tennisexplorer.com/player/roveri-sidney/',
    'Igor Sao Thiago' : 'https://www.tennisexplorer.com/player/sao-thiago/',
    'Carlos Eduardo Severino' : 'https://www.tennisexplorer.com/player/severino-84d9a/',
    'Esteban Bruna' : 'https://www.tennisexplorer.com/player/bruna-45b58/',
    'Osni Junior' : 'https://www.tennisexplorer.com/player/junior-fc746/',
    'Felipe Assuncao Garla' : 'https://www.tennisexplorer.com/player/assuncao-garla/',
    'Caio Zampieri' : 'https://www.tennisexplorer.com/player/zampieri-c72da/',
    'Fabiano De Paula' : 'https://www.tennisexplorer.com/player/de-paula-41b06/',
    "Felipe D'Annunzio" : 'https://www.tennisexplorer.com/player/d-annunzio/',
    'Maxime Teixeira' : 'https://www.tennisexplorer.com/player/teixeira-5d255/',
    'Pedro Bernardi' : 'https://www.tennisexplorer.com/player/bernardi-e47ee/',
    'Marcos Vinicius Dias' : 'https://www.tennisexplorer.com/player/dias-5938f/',
    'Julian Busch' : 'https://www.tennisexplorer.com/player/busch-e963a/',
    'Tomas Buchhass' : 'https://www.tennisexplorer.com/player/buchhass-618f9/',
    'Mauricio Cassimiro' : 'https://www.tennisexplorer.com/player/cassimiro-de-oliveira/',
    'Marcelo Fortini Murbach' : 'https://www.tennisexplorer.com/player/fortini-murbach/',
    'Marcos Bernardes' : 'https://www.tennisexplorer.com/player/bernardes-cd7e5/',
    'Jose Benitez' : 'https://www.tennisexplorer.com/player/benitez-1edc3/',
    'Talles De Oliveira Vilarinho' : 'https://www.tennisexplorer.com/player/de-oliveira-vilarinho/',
    'Javier Munoz' : 'https://www.tennisexplorer.com/player/munoz-06d44/',
    'Vinicius Ono' : 'https://www.tennisexplorer.com/player/ono-3cb05/',
    'Fernando Albuquerque' : 'https://www.tennisexplorer.com/player/albuquerque-528d3/',
    'Victor Amorim Gonzaga' : 'https://www.tennisexplorer.com/player/amorim-gonzaga/',
    'Danilo Ferraz' : 'https://www.tennisexplorer.com/player/ferraz-b0c8c/',
    'Daniel Schmitt' : 'https://www.tennisexplorer.com/player/schmitt-65142/',
    'Lucas Martins Vaz' : 'https://www.tennisexplorer.com/player/martins-vaz/',
    'Silas Araujo de Cerqueira' : 'https://www.tennisexplorer.com/player/araujo-de-cerqueira/',
    'Eric Gomes' : 'https://www.tennisexplorer.com/player/gomes-eaad2/',
    'Lucas Santana' : 'https://www.tennisexplorer.com/player/santana-80bf5/',
    'Anders Lindstrom' : 'https://www.tennisexplorer.com/player/lindstrom-b6046/',
    'Jose Nascimento': 'https://www.tennisexplorer.com/player/nascimento-facd9/',
    'Rodolfo Bustamante' : 'https://www.tennisexplorer.com/player/bustamante-9a944/',
    'Filipe Penteado' : 'https://www.tennisexplorer.com/player/penteado-e15fc/',
    'Federico Abadie' : 'https://www.tennisexplorer.com/player/abadie-df1d8/',
    'Eduardo Furusho' : 'https://www.tennisexplorer.com/player/furusho/',
    'Gustavo Garetto' : 'https://www.tennisexplorer.com/player/garetto/',
    'Jeremy Bates' : 'https://www.tennisexplorer.com/player/bates/',
    'Richard Schmidt' : 'https://www.tennisexplorer.com/player/schmidt/'
}
    



df_keys = df_brasil[df_brasil['PlayerName'].isin(dicionario_jogadores_em_falta.keys())]
unique_keys = df_keys['LinkPlayer'].unique()

for player in unique_keys:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    
    # Itera sobre cada linha associada a este jogador
    for index, row in player_rows.iterrows():
        
        # Obter o nome do jogador
        player_name = row['PlayerName']
        
        # Check if RankPlayer is NaN
        if pd.isnull(row['RankPlayer']):
            # Extract the year from the DateStart column
            year = pd.to_datetime(row['DateStart']).year
            
            # Saltar para a próxima iteração se o nome do jogador não estiver 
            #if player_name not in dicionario_jogadores_em_falta:
             #   continue
            
            # Procurar o url no dicionário
            url = f'{dicionario_jogadores_em_falta[player_name]}' + f'?annual={year}/'
            print(url)
            response = session.get(url)
               
            # Extrair o HTML
            html = response.html.html
            soup = BeautifulSoup(html, "html.parser")
            # Encontrar o elemento current/highest rank for singles
            rank_element = soup.find('div', text=re.compile('Current/Highest rank - singles'))
        #    print(rank_element.text)
            
            if rank_element:
                if 'Current/Highest rank - singles: -' in rank_element.text:      
                    rank_number = re.findall('\d+', rank_element.text)[0]
                    df_brasil.at[index, 'RankPlayer'] = int(rank_number)

                    
                elif 'Current/Highest rank - singles: -' not in rank_element.text:

                    # Extrair o número do elemento
                    rank_number = rank_element.text.split(':')[1].split('.')[0].strip()
   
                    # Atualizar a coluna RankPlayer do DataFrame
                    df_brasil.at[index, 'RankPlayer'] = int(rank_number)
                    
                #else:
                   # print("Bruh")
                   # rank_number = re.findall('\d+', rank_element.text)[0]
                   # print(rank_number)
   
            
            else:
                # Se o rank não é encontrado, mantém-se como NaN no DataFrame
                df_brasil.at[index, 'RankPlayer'] = np.nan
                
                
for i, row in df_brasil[df_brasil['RankPlayer'].isna()].iterrows():
    
    url = row['LinkPlayer'].replace("player-activity?year=all&matchType=Singles", "rankings-history/")
    response = session.get(url)
    print(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="mega-table")
    
   # if table is None:
      #  continue
    thead = table.find("thead")
    tbody = table.find("tbody")
    
    singles_cell_index = None
    
    for i, th in enumerate(thead.find_all("th")):
        
        if th.text.strip() == "Singles":
            singles_cell_index = i
            break
        
    cell_value = None
    
    for tr in tbody.find_all("tr"):
        
        tds = tr.find_all("td")
        date = tds[0].text.strip()
        year = int(date.split(".")[0])
        
        if year == row['DateStart'].year:
            for i, td in enumerate(tds):
                if i == singles_cell_index and td.text.strip() != "0":
                    cell_value = td.text.strip()
                    if not cell_value.isdigit(): # adiciona a condição
                        cell_value = cell_value[:-1] # remove o "T"
                    df_brasil.at[i, 'RankPlayer'] = cell_value
                    break
                
            if cell_value is not None:
                break
            
    if cell_value is None:
        continue
        

        
df_brasil.loc[(df_brasil['PlayerName'] == 'Eduardo Furusho') & 
              (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].apply(lambda x: x.year) == 1985), 
              'RankPlayer'] = 794
       
df_brasil.loc[(df_brasil['PlayerName'] == 'Gustavo Garetto') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].apply(lambda x: x.year) == 1984),
              'RankPlayer'] = 1071

df_brasil.loc[(df_brasil['PlayerName'] == 'Jeremy Bates') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 341

df_brasil.loc[(df_brasil['PlayerName'] == 'Richard Schmidt') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 486

df_brasil.loc[(df_brasil['PlayerName'] == 'Danilo Marcelino') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 563

df_brasil.loc[(df_brasil['PlayerName'] == 'Danilo Marcelino') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 487

df_brasil.loc[(df_brasil['PlayerName'] == 'Fabio Silberberg') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1991), 'RankPlayer'] = 679

df_brasil.loc[(df_brasil['PlayerName'] == 'Fabio Silberberg') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1987), 'RankPlayer'] = 870

df_brasil.loc[(df_brasil['PlayerName'] == 'Fernando Roese') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 258

df_brasil.loc[(df_brasil['PlayerName'] == 'Fernando Roese') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 258

df_brasil.loc[(df_brasil['PlayerName'] == 'Fernando Roese') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 258

df_brasil.loc[(df_brasil['PlayerName'] == 'Vitor Martins') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1992), 'RankPlayer'] = 1077

df_brasil.loc[(df_brasil['PlayerName'] == 'Diego Perez') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 92

df_brasil.loc[(df_brasil['PlayerName'] == 'Martin Jaite') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 285

df_brasil.loc[(df_brasil['PlayerName'] == 'Roberto Azar') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1985), 'RankPlayer'] = 398

df_brasil.loc[(df_brasil['PlayerName'] == 'Cassio Motta') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 86

df_brasil.loc[(df_brasil['PlayerName'] == 'Cassio Motta') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 232

df_brasil.loc[(df_brasil['PlayerName'] == 'Cassio Motta') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 255

df_brasil.loc[(df_brasil['PlayerName'] == 'Cassio Motta') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 99

df_brasil.loc[(df_brasil['PlayerName'] == 'Raul Antonio Viver') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 325

df_brasil.loc[(df_brasil['PlayerName'] == 'Raul Antonio Viver') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 300

df_brasil.loc[(df_brasil['PlayerName'] == 'Jose Daher') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 375

df_brasil.loc[(df_brasil['PlayerName'] == 'Jose Daher') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 527

df_brasil.loc[(df_brasil['PlayerName'] == 'Pablo Arraya') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 83

df_brasil.loc[(df_brasil['PlayerName'] == 'Pablo Arraya') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 309

df_brasil.loc[(df_brasil['PlayerName'] == 'Jose Antonio Fernandez') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 329

df_brasil.loc[(df_brasil['PlayerName'] == 'Cesar Kist') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 445

df_brasil.loc[(df_brasil['PlayerName'] == 'Cesar Kist') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 369

df_brasil.loc[(df_brasil['PlayerName'] == 'Cesar Kist') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 369

df_brasil.loc[(df_brasil['PlayerName'] == 'Cesar Kist') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 369

df_brasil.loc[(df_brasil['PlayerName'] == 'Marko Ostoja') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 172

df_brasil.loc[(df_brasil['PlayerName'] == 'Mark Greenan') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 609

df_brasil.loc[(df_brasil['PlayerName'] == 'Guillermo Vilas') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1972), 'RankPlayer'] = 27

df_brasil.loc[(df_brasil['PlayerName'] == 'Ricardo Rivera') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1985), 'RankPlayer'] = 464

df_brasil.loc[(df_brasil['PlayerName'] == 'Ricardo Rivera') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 295

df_brasil.loc[(df_brasil['PlayerName'] == 'Ricardo Rivera') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 309

df_brasil.loc[(df_brasil['PlayerName'] == 'Ricardo Rivera') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 662

df_brasil.loc[(df_brasil['PlayerName'] == 'Luis Ruette') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1987), 'RankPlayer'] = 563

df_brasil.loc[(df_brasil['PlayerName'] == 'Francisco Maciel') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 138

df_brasil.loc[(df_brasil['PlayerName'] == 'Pedro Rebolledo') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 133

df_brasil.loc[(df_brasil['PlayerName'] == 'Pedro Rebolledo') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 129

df_brasil.loc[(df_brasil['PlayerName'] == 'Pedro Rebolledo') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 300

df_brasil.loc[(df_brasil['PlayerName'] == 'Pedro Rebolledo') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankPlayer'] = 555

df_brasil.loc[(df_brasil['PlayerName'] == 'Eduardo Bengoechea') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 271

df_brasil.loc[(df_brasil['PlayerName'] == 'Eduardo Bengoechea') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 279

df_brasil.loc[(df_brasil['PlayerName'] == 'Eduardo Bengoechea') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 162

df_brasil.loc[(df_brasil['PlayerName'] == 'Eduardo Bengoechea') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 84

df_brasil.loc[(df_brasil['PlayerName'] == 'Juan Aguilera') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 225

df_brasil.loc[(df_brasil['PlayerName'] == 'Ricardo Acioly') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 743

df_brasil.loc[(df_brasil['PlayerName'] == 'Ricardo Acioly') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 743

df_brasil.loc[(df_brasil['PlayerName'] == 'Roberto Arguello') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 365

df_brasil.loc[(df_brasil['PlayerName'] == 'Leif Shiras') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 408

df_brasil.loc[(df_brasil['PlayerName'] == 'Sergio Sarli') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1988), 'RankPlayer'] = 954

df_brasil.loc[(df_brasil['PlayerName'] == 'Sergio Sarli') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1987), 'RankPlayer'] = 756

df_brasil.loc[(df_brasil['PlayerName'] == 'Carlos Chabalgoity') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 343

df_brasil.loc[(df_brasil['PlayerName'] == 'Carlos Chabalgoity') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 415

df_brasil.loc[(df_brasil['PlayerName'] == 'Carlos Chabalgoity') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 415

df_brasil.loc[(df_brasil['PlayerName'] == 'Carlos Chabalgoity') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 415

df_brasil.loc[(df_brasil['PlayerName'] == 'Carlos Chabalgoity') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 415

df_brasil.loc[(df_brasil['PlayerName'] == 'Julio Goes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankPlayer'] = 104

df_brasil.loc[(df_brasil['PlayerName'] == 'Julio Goes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 117

df_brasil.loc[(df_brasil['PlayerName'] == 'Julio Goes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 145

df_brasil.loc[(df_brasil['PlayerName'] == 'Julio Goes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 163

df_brasil.loc[(df_brasil['PlayerName'] == 'Julio Goes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 163

df_brasil.loc[(df_brasil['PlayerName'] == 'Julio Goes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankPlayer'] = 163

df_brasil.loc[(df_brasil['PlayerName'] == 'Givaldo Barbosa') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankPlayer'] = 110

df_brasil.loc[(df_brasil['PlayerName'] == 'Givaldo Barbosa') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankPlayer'] = 99

df_brasil.loc[(df_brasil['PlayerName'] == 'Givaldo Barbosa') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 356

df_brasil.loc[(df_brasil['PlayerName'] == 'Givaldo Barbosa') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankPlayer'] = 356

df_brasil.loc[(df_brasil['PlayerName'] == 'Givaldo Barbosa') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1976), 'RankPlayer'] = 360

df_brasil.loc[(df_brasil['PlayerName'] == 'Mark Buckley') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankPlayer'] = 594

df_brasil.loc[(df_brasil['PlayerName'] == 'Jan Kodes') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1971), 'RankPlayer'] = 9

df_brasil.loc[(df_brasil['PlayerName'] == 'Alexander Merino') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2022), 'RankPlayer'] = 1341

df_brasil.loc[(df_brasil['PlayerName'] == 'Alexander Merino') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankPlayer'] = 2129

df_brasil.loc[(df_brasil['PlayerName'] == 'Arklon Huertas Del Pino Cordova') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2019), 'RankPlayer'] = 612

df_brasil.loc[(df_brasil['PlayerName'] == 'Bruno Santanna') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankPlayer'] = 732

df_brasil.loc[(df_brasil['PlayerName'] == 'Facundo Juarez') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2019), 'RankPlayer'] = 694

df_brasil.loc[(df_brasil['PlayerName'] == 'Gustavo Heide') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2018), 'RankPlayer'] = 1658

df_brasil.loc[(df_brasil['PlayerName'] == 'Leonardo Telles') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankPlayer'] = 1828

df_brasil.loc[(df_brasil['PlayerName'] == 'Leonardo Telles') & (df_brasil['RankPlayer'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankPlayer'] = 1441

df_brasil.loc[(df_brasil['PlayerName'] == 'Rafael Nadal') & (df_brasil['RankPlayer']==1041.0) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankPlayer'] = 5



# Guarda o DataFrame modificado num csv
df_brasil = df_brasil.to_csv('atpplayers_web_scrapped.csv', index=False)
