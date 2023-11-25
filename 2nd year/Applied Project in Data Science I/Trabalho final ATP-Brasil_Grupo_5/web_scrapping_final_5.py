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

session = HTMLSession()

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
    'Richard Schmidt' : 'https://www.tennisexplorer.com/player/schmidt/',
    'Roberto Cid Subervi' : 'https://www.tennisexplorer.com/player/cid-subervi/',
    'Jose Fco. Vidal Azorin' : 'https://www.tennisexplorer.com/player/vidal-azorin/',
    'Tsung-Hua Yang' : 'https://www.tennisexplorer.com/player/yang-90609/',
    'Juan Martin del Potro' : 'https://www.tennisexplorer.com/player/del-potro/',
    'Alex Bogomolov Jr.' : 'https://www.tennisexplorer.com/player/bogomolov/',
    'Jonathan Dasnieres de Veigy' : 'https://www.tennisexplorer.com/player/dasnieres-de-veigy/',
    'Izak Van der Merwe' : 'https://www.tennisexplorer.com/player/van-der-merwe-552d0/',
    'Daniel-Alejandro Lopez Cassaccia' : 'https://www.tennisexplorer.com/player/lopez-cassaccia/',
    "Matias O'Neille" : 'https://www.tennisexplorer.com/player/o-neille/',
    'John van Lottum' : 'https://www.tennisexplorer.com/player/van-lottum-db071/',
    'Juan Gisbert Sr' : 'https://www.tennisexplorer.com/player/gisbert-sr-/',
    'Leonardo Telles' : 'https://www.tennisexplorer.com/player/civita-telles/',
    'Marcelo Zormann' : 'https://www.tennisexplorer.com/player/zormann-45d50/',
    'Kaichi Uchida' : 'https://www.tennisexplorer.com/player/uchida-ea757/',
    # Roman Andres Burruchaga
    # Navonne
}

print("Web scrapping L_OR_R ...\n")

# Obtém uma lista de jogadores únicos
unique_players = df_brasil['LinkPlayer'].unique()

# Inicia uma sessão HTML para fazer solicitações na web
session = HTMLSession()



# Itera sobre cada jogador único
for player in unique_players:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    for index, row in player_rows.iterrows():
        
        # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
        player_rows = df_brasil[df_brasil['LinkPlayer'] == player]

        
        # Verifica se a mão está faltando (NaN) para o jogador atual
        
        if pd.isna(player_rows['L_OR_R'].iloc[0]):
            
            # Obtém os cookies da sessão
            cookies = session.cookies.get_dict()
            
            last_name = row['PlayerName'].split()[-1].lower()
            

            url = f'https://www.tennisexplorer.com/player/{last_name}/'
            
            response = session.get(url, cookies=cookies)
          #  print(url)
            
            html = response.html.html
            
            soup = BeautifulSoup(html, 'html.parser')
            
            hand_elements = soup.find_all(class_='date')
            
            if hand_elements is not None:
                # Percorre todos os elementos encontrados
                for element in hand_elements:
                    
                    # Verifica se o texto do elemento contém "Plays"
                    if "Plays" in element.text:
                        l_or_r = element.text.split(':')[1].split('.')[0].strip()
                        
                        if l_or_r == "right":
                            df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = "Right-Handed"
                            
                        elif l_or_r == "left":
                            df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = "Left-Handed"
                            
            else:
                df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = np.nan
                
                
# Itera sobre cada jogador único
for player in unique_players:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    for index, row in player_rows.iterrows():
        
         player_name = row['PlayerName']
         
         if player_name not in dicionario_jogadores_em_falta.keys():
             continue
         
         if pd.isna(player_rows['L_OR_R'].iloc[0]):
            

            cookies = session.cookies.get_dict()
            
            last_name = row['PlayerName'].split()[-1].lower()
            

            url = f'{dicionario_jogadores_em_falta[player_name]}'
    
            
            response = session.get(url, cookies=cookies)
            print(url)
 
            
            html = response.html.html
            
            soup = BeautifulSoup(html, 'html.parser')
            
            hand_elements = soup.find_all(class_='date')
            
            if hand_elements is not None:
                # Percorre todos os elementos encontrados
                for element in hand_elements:
                    
                    # Verifica se o texto do elemento contém "Plays"
                    if "Plays" in element.text:
                        l_or_r = element.text.split(':')[1].split('.')[0].strip()
                        
                        if l_or_r == "right":
                            df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = "Right-Handed"
                            
                        elif l_or_r == "left":
                            df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = "Left-Handed"
                            
            else:
                df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = np.nan
                
# Itera sobre cada jogador único
for player in unique_players:

    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    print(player)

    # Verifica se a mão está faltando (NaN) para o jogador atual
    if pd.isna(player_rows['L_OR_R'].iloc[0]):

        # Obtém os cookies da sessão
        cookies = session.cookies.get_dict()

        # Faz uma solicitação para a página do jogador, passando os cookies
        response = session.get(player, cookies=cookies)

        # Extrai o HTML resultante
        html = response.html.html

        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html, 'html.parser')

        all_table_values = soup.find_all('div', {'class': 'table-value'})

        # Verifica se a mão foi encontrada
        if all_table_values is not None:

            l_or_r = all_table_values[1].text.split(",")[0].strip()

            # Atualiza o valor da mão para todos os registros associados a este jogador
            df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = l_or_r 
        
        else:
            # Define a mão como 0 caso não seja encontrada para todos os registros associados a este jogador
            df_brasil.loc[df_brasil['LinkPlayer'] == player, 'L_OR_R'] = np.nan               

                
player_names = df_brasil['PlayerName'].unique()
  
                
for player_name in player_names:
    df_brasil.loc[(df_brasil['Oponent'] == player_name) 
                  & (df_brasil['L_OR_R_Opponent'].isnull()), 'L_OR_R_Opponent'] = df_brasil.loc[df_brasil['PlayerName'] == player_name, 'L_OR_R'].values[0]
                


df_brasil = df_brasil.to_csv('atpplayers_web_scrapped.csv', index=False)