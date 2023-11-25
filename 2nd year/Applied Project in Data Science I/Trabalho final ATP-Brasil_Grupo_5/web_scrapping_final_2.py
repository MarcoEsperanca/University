import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import numpy as np

df_brasil = pd.read_csv('atpplayers_web_scrapped.csv')

df_brasil['DateStart'] = pd.to_datetime(df_brasil['DateStart'])
df_brasil['DateEnd'] = pd.to_datetime(df_brasil['DateEnd'])

# Obtém uma lista de jogadores únicos
unique_players = df_brasil['LinkPlayer'].unique()

# Inicia uma sessão HTML para fazer solicitações na web
session = HTMLSession()

################################################################ RankOpponent #################################################################


df_brasil['Year'] = df_brasil['DateStart'].dt.year

# Criar DataFrame filtrado sem duplicatas
df_filtered = df_brasil.drop_duplicates(subset=("PlayerName", "Oponent", "Year"))

# Iterar sobre as linhas do DataFrame filtrado
for i, row in df_filtered.iterrows():
    # Se o RankOpponent é nulo, buscar o valor no campo RankPlayer para o mesmo jogador
    if pd.isnull(row['RankOpponent']):
        same_player = df_filtered[(df_filtered['PlayerName'] == row['Oponent']) & (df_filtered['DateStart'].dt.year == row['DateStart'].year)]
        if not same_player.empty:
            # Atualizar o valor de RankOpponent apenas se for nulo
            if pd.isnull(df_brasil.loc[i, 'RankOpponent']):
                df_brasil.loc[i, 'RankOpponent'] = same_player.iloc[0]['RankPlayer']
                
                
print("Web scrapping RankOpponent ...\n")

# Itera sobre cada linha dos links únicos
for player in unique_players:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    
    # Itera sobre cada linha associada a este jogador
    for index, row in player_rows.iterrows():
        
        # Check if RankOpponent is NaN
        if pd.isnull(row['RankOpponent']):
            # Extract the year from the DateStart column
            year = pd.to_datetime(row['DateStart']).year
          
            # Extract the player's last name from the Oponent column
            last_name = row['Oponent'].split()[-1].lower()
            
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
                    df_brasil.at[index, 'RankOpponent'] = int(rank_number)

                    
                elif 'Current/Highest rank - singles: -' not in rank_element.text:

                    # Extrair o número do elemento
                    rank_number = rank_element.text.split(':')[1].split('.')[0].strip()
   
                    # Atualizar a coluna RankOpponent do DataFrame
                    df_brasil.at[index, 'RankOpponent'] = int(rank_number)
                    
                #else:
                   # print("Bruh")
                   # rank_number = re.findall('\d+', rank_element.text)[0]
                   # print(rank_number)
   
            
            else:
                # Se o rank não é encontrado, mantém-se como NaN no DataFrame
                df_brasil.at[index, 'RankOpponent'] = np.nan
            

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
    



df_keys = df_brasil[df_brasil['Oponent'].isin(dicionario_jogadores_em_falta.keys())]
unique_keys = df_keys['LinkPlayer'].unique()

for player in unique_keys:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    
    # Itera sobre cada linha associada a este jogador
    for index, row in player_rows.iterrows():
        
        # Obter o nome do jogador
        player_name = row['Oponent']
        
        # Check if RankOpponent is NaN
        if pd.isnull(row['RankOpponent']):
            # Extract the year from the DateStart column
            year = pd.to_datetime(row['DateStart']).year
            
            # Saltar para a próxima iteração se o nome do jogador não estiver 
            #if player_name not in dicionario_jogadores_em_falta:
             #   continue
            
            # Procurar o url no dicionário
            if player_name in dicionario_jogadores_em_falta.keys():
                url = f'{dicionario_jogadores_em_falta[player_name]}' + f'?annual={year}/'
            else:
                continue
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
                    df_brasil.at[index, 'RankOpponent'] = int(rank_number)

                    
                elif 'Current/Highest rank - singles: -' not in rank_element.text:

                    # Extrair o número do elemento
                    rank_number = rank_element.text.split(':')[1].split('.')[0].strip()
   
                    # Atualizar a coluna RankOpponent do DataFrame
                    df_brasil.at[index, 'RankOpponent'] = int(rank_number)
                    
                #else:
                   # print("Bruh")
                   # rank_number = re.findall('\d+', rank_element.text)[0]
                   # print(rank_number)
   
            
            else:
                # Se o rank não é encontrado, mantém-se como NaN no DataFrame
                df_brasil.at[index, 'RankOpponent'] = np.nan
                
        
                
                
for i, row in df_brasil[df_brasil['RankOpponent'].isna()].iterrows():
    
    url = row['LinkPlayer'].replace("player-activity?year=all&matchType=Singles", "rankings-history/")
    response = session.get(url)
    print(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="mega-table")
    if table is None:
        continue
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
                    df_brasil.at[i, 'RankOpponent'] = cell_value
                    break
                
            if cell_value is not None:
                break
            
    if cell_value is None:
        continue
    
df_brasil.loc[(df_brasil['Oponent'] == 'Adolfo Aires') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 1432

df_brasil.loc[(df_brasil['Oponent'] == 'Alejandro Gattiker') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 232

df_brasil.loc[(df_brasil['Oponent'] == 'Alejandro Gattiker') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 194

df_brasil.loc[(df_brasil['Oponent'] == 'Alejandro Gattiker') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 511

df_brasil.loc[(df_brasil['Oponent'] == 'Alejandro Gattiker') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 246

df_brasil.loc[(df_brasil['Oponent'] == 'Alejandro Padilha') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1324

df_brasil.loc[(df_brasil['Oponent'] == 'Alejandro Rott') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 2214

df_brasil.loc[(df_brasil['Oponent'] == 'Alexander Glikas') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1992), 'RankOpponent'] = 1124

df_brasil.loc[(df_brasil['Oponent'] == 'Alexandre Aragon') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1537

df_brasil.loc[(df_brasil['Oponent'] == 'Alexandre Aragon') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1732

df_brasil.loc[(df_brasil['Oponent'] == 'Alexandre Prado') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1732

df_brasil.loc[(df_brasil['Oponent'] == 'Alexandre Prado') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1732

df_brasil.loc[(df_brasil['Oponent'] == 'Alexandre Sola') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 2002

df_brasil.loc[(df_brasil['Oponent'] == 'Alexsandro Porfiriio') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 2054

df_brasil.loc[(df_brasil['Oponent'] == 'Alexsandro Porfiriio') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 2054

df_brasil.loc[(df_brasil['Oponent'] == 'Alvaro Betancur') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankOpponent'] = 184

df_brasil.loc[(df_brasil['Oponent'] == 'Americo Lanzoni') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1460

df_brasil.loc[(df_brasil['Oponent'] == 'Americo Lanzoni') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1460

df_brasil.loc[(df_brasil['Oponent'] == 'Americo Lanzoni') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1460

df_brasil.loc[(df_brasil['Oponent'] == 'Americo Lanzoni') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1460

df_brasil.loc[(df_brasil['Oponent'] == 'Americo Lanzoni') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 1460

df_brasil.loc[(df_brasil['Oponent'] == 'Amnon Felipe') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2021), 'RankOpponent'] = 1095

df_brasil.loc[(df_brasil['Oponent'] == 'Andre Cervelatti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 1097

df_brasil.loc[(df_brasil['Oponent'] == 'Andre Luiz Cezar') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1547

df_brasil.loc[(df_brasil['Oponent'] == 'Andre Moreira') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 1680

df_brasil.loc[(df_brasil['Oponent'] == 'Andres Molina') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 302

df_brasil.loc[(df_brasil['Oponent'] == 'Andres Molina') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 302

df_brasil.loc[(df_brasil['Oponent'] == 'Andres Molina') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankOpponent'] = 602

df_brasil.loc[(df_brasil['Oponent'] == 'Andrews Wilson-Moraes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1400

df_brasil.loc[(df_brasil['Oponent'] == 'Andy McCurry') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 480

df_brasil.loc[(df_brasil['Oponent'] == 'Angel Gimenez') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 91

df_brasil.loc[(df_brasil['Oponent'] == 'Antonin Scaff Haddad Bartos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1518

df_brasil.loc[(df_brasil['Oponent'] == 'Antonin Scaff Haddad Bartos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1518

df_brasil.loc[(df_brasil['Oponent'] == 'Antonin Scaff Haddad Bartos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1518

df_brasil.loc[(df_brasil['Oponent'] == 'Antonio Amaro') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 2537

df_brasil.loc[(df_brasil['Oponent'] == 'Antonio Marquez') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1996), 'RankOpponent'] = 1323

df_brasil.loc[(df_brasil['Oponent'] == 'Antonio Morandini') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 826

df_brasil.loc[(df_brasil['Oponent'] == 'Antonio Nascimento') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1997

df_brasil.loc[(df_brasil['Oponent'] == 'Antonio Passaro') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1588

df_brasil.loc[(df_brasil['Oponent'] == 'Bernardo Lipschitz') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1122

df_brasil.loc[(df_brasil['Oponent'] == 'Bernardo Mello Madeira Coelho') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1323

df_brasil.loc[(df_brasil['Oponent'] == 'Bernardo Peixoto Bertolucci') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1783

df_brasil.loc[(df_brasil['Oponent'] == 'Bernardo Peixoto Bertolucci') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1783

df_brasil.loc[(df_brasil['Oponent'] == 'Braulino Silva Jr.') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1998), 'RankOpponent'] = 1567

df_brasil.loc[(df_brasil['Oponent'] == 'Breno Lodis') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2018), 'RankOpponent'] = 1204

df_brasil.loc[(df_brasil['Oponent'] == 'Breno Lodis') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1204

df_brasil.loc[(df_brasil['Oponent'] == 'Breno Lodis') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1204

df_brasil.loc[(df_brasil['Oponent'] == 'Breno Lodis') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2015), 'RankOpponent'] = 1204

df_brasil.loc[(df_brasil['Oponent'] == 'Bruce Kleege') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 154

df_brasil.loc[(df_brasil['Oponent'] == 'Bruce Kleege') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 201

df_brasil.loc[(df_brasil['Oponent'] == 'Bruce Kleege') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 274

df_brasil.loc[(df_brasil['Oponent'] == 'Brunno Barbosa') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1523

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Bertolucci') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1788

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Denadae Biroche') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1788

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Fernandez') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2022), 'RankOpponent'] = 687

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Fernandez') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2021), 'RankOpponent'] = 967

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Figlia') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1871

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Hertwig') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2005), 'RankOpponent'] = 1578

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Hertwig') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1578

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Pessoa') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 1345

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Prates') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1777

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Sapienza') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1152

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Scacallossi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 1452

df_brasil.loc[(df_brasil['Oponent'] == 'Bruno Scacallossi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2005), 'RankOpponent'] = 1452

df_brasil.loc[(df_brasil['Oponent'] == 'Bryan Aguiar Kuntz') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2021), 'RankOpponent'] = 804

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Aguiar') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1121

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Claudino') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 830

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Gomes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1415

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Laureano') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 2057

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Nunes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1344

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Nunes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1344

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Piacentini') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1620

df_brasil.loc[(df_brasil['Oponent'] == 'Caio Rocha Martins') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1712

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Castellan') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 122

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Castellan') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 180

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Castellan') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 179

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Henrique Hooper') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2015), 'RankOpponent'] = 1723

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Horta') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1989), 'RankOpponent'] = 1095

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Lando') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 662

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Lando') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 662

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Matos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2001), 'RankOpponent'] = 1023

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Nedel') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1023

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Nedel') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1027

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Nedel') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2005), 'RankOpponent'] = 1024

df_brasil.loc[(df_brasil['Oponent'] == 'Carlos Thim') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1024

df_brasil.loc[(df_brasil['Oponent'] == 'Caue Gimenez') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1703

df_brasil.loc[(df_brasil['Oponent'] == 'Celso Sacomandi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 510

df_brasil.loc[(df_brasil['Oponent'] == 'Celso Sacomandi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 339

df_brasil.loc[(df_brasil['Oponent'] == 'Celso Sacomandi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankOpponent'] = 339

df_brasil.loc[(df_brasil['Oponent'] == 'Cesar Grobel') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1712

df_brasil.loc[(df_brasil['Oponent'] == 'Cesare Casali') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1023

df_brasil.loc[(df_brasil['Oponent'] == 'Cesare Casali') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1075

df_brasil.loc[(df_brasil['Oponent'] == 'Christophe Freyss') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 82

df_brasil.loc[(df_brasil['Oponent'] == 'Christopher Sylvan') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankOpponent'] = 243

df_brasil.loc[(df_brasil['Oponent'] == 'Ciro Nishiyama') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1990), 'RankOpponent'] = 992

df_brasil.loc[(df_brasil['Oponent'] == 'Claudio Kligerman') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1072

df_brasil.loc[(df_brasil['Oponent'] == 'Claudio Panatta') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 153

df_brasil.loc[(df_brasil['Oponent'] == 'Craig Wittus') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 400

df_brasil.loc[(df_brasil['Oponent'] == 'Craig Wittus') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1984), 'RankOpponent'] = 162

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Baraldi Marcos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1517

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Baraldi Marcos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1517

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Bustamante') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1812

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Coelho') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 997

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel De Boer') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 814

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel De Boer') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 814

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel De Boer') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 814

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Rebelo') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2021), 'RankOpponent'] = 1076

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Schmidt') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 985

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Souza') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1996), 'RankOpponent'] = 1291

df_brasil.loc[(df_brasil['Oponent'] == 'Daniel Viana') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1090

df_brasil.loc[(df_brasil['Oponent'] == 'Dave Siegler') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankOpponent'] = 137

df_brasil.loc[(df_brasil['Oponent'] == 'Davi Guimaraes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1970

df_brasil.loc[(df_brasil['Oponent'] == 'David Dowlen') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 301

df_brasil.loc[(df_brasil['Oponent'] == 'David Maciel Cavalcanti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 789

df_brasil.loc[(df_brasil['Oponent'] == 'David Maciel Cavalcanti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 783

df_brasil.loc[(df_brasil['Oponent'] == 'Denis Jaquetti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1223

df_brasil.loc[(df_brasil['Oponent'] == 'Diego Cavalcanti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1023

df_brasil.loc[(df_brasil['Oponent'] == 'Diego Riviere Padilha') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2018), 'RankOpponent'] = 146

df_brasil.loc[(df_brasil['Oponent'] == 'Diogo Alves Casa') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 569

df_brasil.loc[(df_brasil['Oponent'] == 'Diogo Alves Casa') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 569

df_brasil.loc[(df_brasil['Oponent'] == 'Douglas Wilges') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 920

df_brasil.loc[(df_brasil['Oponent'] == 'Eber Tiepermann') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1038

df_brasil.loc[(df_brasil['Oponent'] == 'Edgar Schurmann') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 511

df_brasil.loc[(df_brasil['Oponent'] == 'Edio Castanhel Filho') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1010

df_brasil.loc[(df_brasil['Oponent'] == 'Edson Krause') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 453

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Assumpcao') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 2007

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Assumpcao') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1577

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Burgui') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1678

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Cavasotti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2001), 'RankOpponent'] = 1528

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Giordani') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1712

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Miquelino') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1970

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Miquelino') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1970

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Oliveira Felter') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1090

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Oliveira Felter') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1090

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Oliveira Felter') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1093

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Santana') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1222

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Saratt') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 335

df_brasil.loc[(df_brasil['Oponent'] == 'Eduardo Taiguara') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2019), 'RankOpponent'] = 430

df_brasil.loc[(df_brasil['Oponent'] == 'Egan Adams') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 1638

df_brasil.loc[(df_brasil['Oponent'] == 'Eidy Igarashi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2001), 'RankOpponent'] = 1524

df_brasil.loc[(df_brasil['Oponent'] == 'Eidy Igarashi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2003), 'RankOpponent'] = 1524

df_brasil.loc[(df_brasil['Oponent'] == 'Eidy Igarashi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 1524

df_brasil.loc[(df_brasil['Oponent'] == 'Elio Jose Ribeiro Lago') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2015), 'RankOpponent'] = 1081

df_brasil.loc[(df_brasil['Oponent'] == 'Emiliano Castellucci') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 790

df_brasil.loc[(df_brasil['Oponent'] == 'Enzo Kohn') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 721

df_brasil.loc[(df_brasil['Oponent'] == 'Enzo Kohn') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1512

df_brasil.loc[(df_brasil['Oponent'] == 'Eric Deblicker') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 128

df_brasil.loc[(df_brasil['Oponent'] == 'Eric Komati') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1465

df_brasil.loc[(df_brasil['Oponent'] == 'Eric Komati') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1465

df_brasil.loc[(df_brasil['Oponent'] == 'Erick Gomes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1998), 'RankOpponent'] = 712

df_brasil.loc[(df_brasil['Oponent'] == 'Erick Gomes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1997), 'RankOpponent'] = 712

df_brasil.loc[(df_brasil['Oponent'] == 'Erick Gomes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1996), 'RankOpponent'] = 712

df_brasil.loc[(df_brasil['Oponent'] == 'Erick Gomes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1993), 'RankOpponent'] = 712

df_brasil.loc[(df_brasil['Oponent'] == 'Erick Iskersky') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 219

df_brasil.loc[(df_brasil['Oponent'] == 'Erick Sgambatti') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1612

df_brasil.loc[(df_brasil['Oponent'] == 'Ernie Fernandez') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 398

df_brasil.loc[(df_brasil['Oponent'] == 'Euler Fanton') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1001

df_brasil.loc[(df_brasil['Oponent'] == 'Euler Fanton') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1054

df_brasil.loc[(df_brasil['Oponent'] == 'Fabiano Queiroz') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1011

df_brasil.loc[(df_brasil['Oponent'] == 'Fabio Minami') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 812

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Baptista') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 912

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Caus') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1213

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Caus') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1114

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Coelho') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1114

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Muzzi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1212

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Russo') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 598

df_brasil.loc[(df_brasil['Oponent'] == 'Felipe Tamayo') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 812

df_brasil.loc[(df_brasil['Oponent'] == 'Fernando Fittipaldi') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 641

df_brasil.loc[(df_brasil['Oponent'] == 'Fernando Gentil') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1976), 'RankOpponent'] = 272

df_brasil.loc[(df_brasil['Oponent'] == 'Fernando Lourenco') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 560

df_brasil.loc[(df_brasil['Oponent'] == 'Fernando Mussolini') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 708

df_brasil.loc[(df_brasil['Oponent'] == 'Fernando Tardin') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2018), 'RankOpponent'] = 456

df_brasil.loc[(df_brasil['Oponent'] == 'Filip Krajcik') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 420

df_brasil.loc[(df_brasil['Oponent'] == 'Flavio Arenzon') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 415

df_brasil.loc[(df_brasil['Oponent'] == 'Francis William Yoshimoto') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2001), 'RankOpponent'] = 1381

df_brasil.loc[(df_brasil['Oponent'] == 'Franco Echenique') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1231

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Franco') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2003), 'RankOpponent'] = 1361

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Franco') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 1433

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Marcolino') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1437

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Marcolino') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1437

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Marcolino') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1237

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Martins') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1237

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Mattos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 363

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Mattos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 363

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Mattos') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankOpponent'] = 347

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Nery') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 969

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Nery') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 969

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Ries') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 989

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Ries') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 985

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Ries') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 986

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Vallim') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 1255

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel Vallim') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1255

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel de Andrade Bendazoli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1689

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel de Andrade Bendazoli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1689

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel de Andrade Bendazoli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1689

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel de Andrade Bendazoli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2015), 'RankOpponent'] = 1585

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel de Andrade Bendazoli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 1589

df_brasil.loc[(df_brasil['Oponent'] == 'Gabriel de Andrade Bendazoli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2018), 'RankOpponent'] = 1589

df_brasil.loc[(df_brasil['Oponent'] == 'Ghilherme Scarpelli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1276

df_brasil.loc[(df_brasil['Oponent'] == 'Ghilherme Scarpelli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1276

df_brasil.loc[(df_brasil['Oponent'] == 'Ghilherme Scarpelli') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1276

df_brasil.loc[(df_brasil['Oponent'] == 'Giovanni Nascimento') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2003), 'RankOpponent'] = 1171

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Destefani') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1255

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Destefani') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1989

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Destefani') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1489

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Dumit') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1489

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Gesser') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1321

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Gesser') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1121

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Inaimo') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1440

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Rebolo') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1440

df_brasil.loc[(df_brasil['Oponent'] == 'Guilherme Toresan') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2018), 'RankOpponent'] = 1044

df_brasil.loc[(df_brasil['Oponent'] == 'Guillermo Aubone') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 321

df_brasil.loc[(df_brasil['Oponent'] == 'Guillermo Aubone') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 133

df_brasil.loc[(df_brasil['Oponent'] == 'Guillermo Aubone') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 191

df_brasil.loc[(df_brasil['Oponent'] == 'Guillermo Nicol') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1412

df_brasil.loc[(df_brasil['Oponent'] == 'Gustavo Holz') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1077

df_brasil.loc[(df_brasil['Oponent'] == 'Gustavo Holz') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1015

df_brasil.loc[(df_brasil['Oponent'] == 'Gustavo Lima Robson') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1019

df_brasil.loc[(df_brasil['Oponent'] == 'Gustavo Lima Robson') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1219

df_brasil.loc[(df_brasil['Oponent'] == "Gustavo Miele d'Ascenzi") & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1219

df_brasil.loc[(df_brasil['Oponent'] == 'Gustavo Moreira') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2015), 'RankOpponent'] = 1017

df_brasil.loc[(df_brasil['Oponent'] == 'Gustavo Puga') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 1020

df_brasil.loc[(df_brasil['Oponent'] == 'Hatteros Pires-Sarnicola') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1122

df_brasil.loc[(df_brasil['Oponent'] == 'Heinz Gildemeister') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 235

df_brasil.loc[(df_brasil['Oponent'] == 'Helio Guedes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 689

df_brasil.loc[(df_brasil['Oponent'] == 'Helmut Leyva') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2005), 'RankOpponent'] = 1012

df_brasil.loc[(df_brasil['Oponent'] == 'Henrique Boturao') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2007), 'RankOpponent'] = 1012

df_brasil.loc[(df_brasil['Oponent'] == 'Henrique Cancado') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1529

df_brasil.loc[(df_brasil['Oponent'] == 'Henrique Fukushima') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2019), 'RankOpponent'] = 1485

df_brasil.loc[(df_brasil['Oponent'] == 'Henrique Norbiato') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2006), 'RankOpponent'] = 1485

df_brasil.loc[(df_brasil['Oponent'] == 'Henrique Silvestre Gomes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2021), 'RankOpponent'] = 2125

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Cesar Dojas') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1358

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Cesar Dojas') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1355

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Cesar Dojas') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1362

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Roverano') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 457

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Roverano') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 457

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Scott') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 365

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Simoes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 888

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Varela') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1979), 'RankOpponent'] = 210

df_brasil.loc[(df_brasil['Oponent'] == 'Hugo Werneck') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1992), 'RankOpponent'] = 1085

df_brasil.loc[(df_brasil['Oponent'] == 'Iago Guerin') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1185

df_brasil.loc[(df_brasil['Oponent'] == 'Igor Candia') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2008), 'RankOpponent'] = 1185

df_brasil.loc[(df_brasil['Oponent'] == 'Igor Schattan') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2013), 'RankOpponent'] = 1342

df_brasil.loc[(df_brasil['Oponent'] == 'Ivan Camus') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1982), 'RankOpponent'] = 1342

df_brasil.loc[(df_brasil['Oponent'] == 'Ivan Camus') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1981), 'RankOpponent'] = 1341

df_brasil.loc[(df_brasil['Oponent'] == 'Ivan Marreiros Da Costa Filho') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1011

df_brasil.loc[(df_brasil['Oponent'] == 'Ivo Rischbieter Jr.') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1011

df_brasil.loc[(df_brasil['Oponent'] == 'Ivo Souto') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2004), 'RankOpponent'] = 1511

df_brasil.loc[(df_brasil['Oponent'] == 'Jair Montovani') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1998), 'RankOpponent'] = 381

df_brasil.loc[(df_brasil['Oponent'] == 'Javier Angel Ignacio Ahumada Garrido') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1421

df_brasil.loc[(df_brasil['Oponent'] == 'Jeff Robbins') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1980), 'RankOpponent'] = 480

df_brasil.loc[(df_brasil['Oponent'] == 'Jeff Turpin') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1983), 'RankOpponent'] = 343

df_brasil.loc[(df_brasil['Oponent'] == 'Joacir Campigotto Jr.') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 1247

df_brasil.loc[(df_brasil['Oponent'] == 'Joacir Campigotto Jr.') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1247

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Batista de Pontes') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2011), 'RankOpponent'] = 1201

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Camara') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1458

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Gabriel Velloso') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 252

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Gabriel Velloso') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 252

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Paulo Menano') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 1998), 'RankOpponent'] = 1000

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Pedro Alcantara') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2017), 'RankOpponent'] = 1201

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Pedro Duarte') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2010), 'RankOpponent'] = 1060

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Pedro Duarte') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2009), 'RankOpponent'] = 1089

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Pedro Ostermayer') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2012), 'RankOpponent'] = 788

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Pedro Tayar') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 889

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Victor Amato Trindade') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2014), 'RankOpponent'] = 1074

df_brasil.loc[(df_brasil['Oponent'] == 'Joao Vitor Prado Festa') & (df_brasil['RankOpponent'].isna()) & 
              (df_brasil['DateStart'].dt.year == 2016), 'RankOpponent'] = 712
















# Guarda o DataFrame modificado num csv
df_brasil = df_brasil.to_csv('atpplayers_web_scrapped.csv', index=False)