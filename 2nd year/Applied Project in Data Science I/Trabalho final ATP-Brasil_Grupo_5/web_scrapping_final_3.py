import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import numpy as np
import datetime

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
    'Marcelo Zormann' : 'https://www.tennisexplorer.com/player/zormann-45d50/'
}
   

# Itera sobre cada jogador único
for player in unique_players:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    for index, row in player_rows.iterrows():
        
        # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
        player_rows = df_brasil[df_brasil['LinkPlayer'] == player]

        
        # Verifica se a altura está faltando (NaN) para o jogador atual
        
        if pd.isna(player_rows['Birthday'].iloc[0]):
            
            # Obtém os cookies da sessão
            cookies = session.cookies.get_dict()
            
            last_name = row['PlayerName'].split()[-1].lower()
            

            url = f'https://www.tennisexplorer.com/player/{last_name}/'
            
            response = session.get(url, cookies=cookies)
            print(url)
            
            html = response.html.html
            
            soup = BeautifulSoup(html, 'html.parser')
            
            birthday = soup.find("div", {"class": "date"}, string=lambda s: "Age" in s)
            
            if birthday is not None:
                birthday = birthday.text.split(" (")[1].replace("(", "").replace(")", "").strip()
                dt = datetime.datetime.strptime(birthday, "%d. %m. %Y")
                formatted_birthday = dt.strftime("%Y-%m-%d")
                dt_formatted = datetime.datetime.strptime(formatted_birthday, "%Y-%m-%d").date()
                df_brasil.loc[df_brasil['LinkPlayer'] == player, 'Birthday'] = dt_formatted
            
            else:
                df_brasil.loc[df_brasil['LinkPlayer'] == player, 'Birthday'] = np.nan
            


# Itera sobre cada jogador único
for player in unique_players:
    
    # Filtra o DataFrame para obter apenas as linhas associadas a este jogador
    player_rows = df_brasil[df_brasil['LinkPlayer'] == player]
    
    for index, row in player_rows.iterrows():
        
         player_name = row['PlayerName']
         
         if player_name not in dicionario_jogadores_em_falta.keys():
             continue
         
         if pd.isna(player_rows['Birthday'].iloc[0]):
            

            cookies = session.cookies.get_dict()
            
            last_name = row['PlayerName'].split()[-1].lower()
            

            url = f'{dicionario_jogadores_em_falta[player_name]}'
    
            
            response = session.get(url, cookies=cookies)
            print(url)
 
            
            html = response.html.html
            
            soup = BeautifulSoup(html, 'html.parser')
            
            birthday = soup.find("div", {"class": "date"}, string=lambda s: "Age" in s)
            
            if birthday is not None:
                birthday = birthday.text.split(" (")[1].replace("(", "").replace(")", "").strip()
                dt = datetime.datetime.strptime(birthday, "%d. %m. %Y")
                formatted_birthday = dt.strftime("%Y-%m-%d")
                dt_formatted = datetime.datetime.strptime(formatted_birthday, "%Y-%m-%d").date()
                df_brasil.loc[df_brasil['LinkPlayer'] == player, 'Birthday'] = dt_formatted
            
            else:
                df_brasil.loc[df_brasil['LinkPlayer'] == player, 'Birthday'] = np.nan
            
df_brasil.loc[df_brasil['PlayerName'] == 'Jhonathan Medina-Alvarez', 'Birthday'] = '1982-12-01'

df_brasil.loc[df_brasil['PlayerName'] == 'Moacir Santos-Filho', 'Birthday'] = '1987-02-25'

df_brasil.loc[df_brasil['PlayerName'] == 'Geronimo Degreef', 'Birthday'] = '1970-03-27'

df_brasil.loc[df_brasil['PlayerName'] == 'Jose-Luis Clerc', 'Birthday'] = '1958-08-16'

df_brasil.loc[df_brasil['PlayerName'] == 'Luis Ruette', 'Birthday'] = '1970-03-27'

df_brasil.loc[df_brasil['PlayerName'] == 'Alfonso Fernandez-Fermoselle', 'Birthday'] = '1971-09-16'

df_brasil.loc[df_brasil['PlayerName'] == 'Richard Lubner', 'Birthday'] = '1967-05-13'

df_brasil.loc[df_brasil['PlayerName'] == 'Juan Pablo Etchecoin', 'Birthday'] = '1969-05-13'

df_brasil.loc[df_brasil['PlayerName'] == 'Stefan Dallwitz', 'Birthday'] = '1965-02-07'

df_brasil.loc[df_brasil['PlayerName'] == 'Gerardo Vacarezza', 'Birthday'] = '1965-08-16'

df_brasil.loc[df_brasil['PlayerName'] == 'Carlos Chabalgoity', 'Birthday'] = '1965-02-02'

df_brasil.loc[df_brasil['PlayerName'] == 'Hatem McDadi', 'Birthday'] = '1960-01-05'


################################################################ BirthdayOpponent #################################################################

player_names = df_brasil['PlayerName'].unique()

for player_name in player_names:
    df_brasil.loc[(df_brasil['Oponent'] == player_name) 
                  & (df_brasil['BirthdayOpponent'].isnull()), 'BirthdayOpponent'] = df_brasil.loc[df_brasil['PlayerName'] == player_name, 'Birthday'].values[0]

            
# Guarda o DataFrame modificado num csv
df_brasil = df_brasil.to_csv('atpplayers_web_scrapped.csv', index=False)
                      