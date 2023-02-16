from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from functions import *
from time import sleep
from datetime import datetime
import sys
import os
import math
import unicodedata
import pandas as pd
from pprint import pprint

url = 'https://digital.stf.jus.br/publico/publicacoes'
PATH_DRIVER = 'chromedriver.exe'
# Apresentar o número de registros encontrados e baixados

date_hour_start = datetime.today().strftime('%d/%m/%Y %H:%M')

print('OPÇÕES DE PROGRAMAS: \n1 - Novo Arquivo \n2 - Arquivo existente\n')
menu_opcoes = input('Escolha uma opção: ')
if menu_opcoes == '2':
    continuar_parametro()

data = input('Escolha uma data no padrão DD/MM/AAAA: ')
print('')
data_split = data.split('/')
dia = data_split[0]
mes = data_split[1]
ano = data_split[2]
time_pd = f'{ano}-{mes}-{dia}'
timestamp = pd.Timestamp(time_pd)
name_day = timestamp.day_name()
dia_da_semana = day_of_week(name_day)
nome_mes = name_month(mes)

validar = True
while  validar:
    sleep(0.5)
    print('OPÇÕES DE BUSCA: \n1 - Publicação \n2 - Divulgação \n3 - Sair do Programa\n')
    opcao_site = input('Escolha uma opção: ')

    if opcao_site == '1':
        sleep(0.5)
        print('Você escolheu a opção Publicação')
        opcao_texto = 'Publicação'
        validar = False
    elif opcao_site == '2':
        sleep(0.5)
        print('Você escolheu a opção Divulgação')
        opcao_texto = 'Divulgação'
        validar = False
    elif opcao_site == '3':
        sleep(0.5)
        print('Saindo do Programa!')
        sleep(0.5)
        exit()
    else:
        sleep(0.5)
        print('\033[31m'+'Opção Inválida!'+'\033[0;0m'+'\n')
    
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

chrome = webdriver.Chrome(options=options)
chrome.get(url)

sleep(5)

# Abrir arquivo
caminho_arquivo = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}.txt'
nome_arquivo = f'STFSITE-{ano}.{mes}.{dia}.txt'
caminho_resumo = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}-Resumo.txt'
caminho_num_processos = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}-NumProcessos.txt'

# Gerando arquivo que contém somente os números dos processos
num_processos_file = open(caminho_num_processos, 'w')
num_processos_file.write(caminho_num_processos + '\n')
num_processos_file.write('=' * 54 + '\n')

# Gerando o arquivo de resumo
with open(caminho_resumo, 'w') as resumo:
    first_row = f'STFSITE: {opcao_texto}: {dia}/{mes}/{ano} ARQUIVO: {nome_arquivo}'
    resumo.write(first_row + '\n')

# Gerando o arquivo que contém os dados dos processos
with open(caminho_arquivo, 'w') as txt:
    cabecalho = f'{opcao_texto}: {dia_da_semana}, {dia} de {nome_mes} de {ano} - STF - SITE'
    site = 'SITE DO STF'
    txt.write(cabecalho + '\n')
    txt.write(site + '\n')

    # Chamar função que define a data e escolhe a opção publicação ou divulgação
    set_date(data, opcao_texto, chrome)
    sleep(2)

    # Pegar quantos registros foram encontrados
    registros = chrome.find_element(By.CLASS_NAME, 'dataTables_info')
    html_registros = registros.get_attribute('outerHTML')
    soup_registros = BeautifulSoup(html_registros, 'html.parser')
    num_processos = soup_registros.get_text().split(' ')[1]

    # Definir o numero de vezes que ira percorrer as paginas
    range_loop = int(num_processos) / 10
    range_loop = math.ceil(range_loop)

    # Print on the screen the number of pages and registers
    print(f'\nForam encontrados {num_processos} registros em {range_loop} páginas!')
sleep(20)
chrome.close()