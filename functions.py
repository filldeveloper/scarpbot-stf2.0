from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
from bs4 import BeautifulSoup
import math
import unicodedata
import pandas as pd
from time import sleep
from datetime import datetime
import codecs

def outer_html(html_element):
    try:
        try:
            html_content_elem = html_element.get_attribute('outerHTML')
        except:
            html_content_elem = html_element.get_attribute('outerHTML')
    except:
        try:
            html_content_elem = html_element.get_attribute('outerHTML')
        except:
            html_content_elem = html_element.get_attribute('outerHTML')
    soup_elem= BeautifulSoup(html_content_elem, 'html.parser')
    texto = soup_elem.get_text('')

    return texto

def day_of_week(nome_dia):
    if nome_dia == 'Sunday':
        dia_da_semana = 'Domingo'
    elif nome_dia == 'Monday':
        dia_da_semana = 'Segunda-feira'
    elif nome_dia == 'Tuesday':
        dia_da_semana = 'Terça-feira'
    elif nome_dia == 'Wednesday':
        dia_da_semana = 'Quarta-feira'
    elif nome_dia == 'Thursday':
        dia_da_semana = 'Quinta-feira'
    elif nome_dia == 'Friday':
        dia_da_semana = 'Sexta-feira'
    else:
        dia_da_semana = 'Sábado'

    return dia_da_semana

def name_month(mes):
    if mes == '01':
        nome_mes = 'Janeiro'
    elif mes == '02':
        nome_mes = 'Fevereiro'
    elif mes == '03':
        nome_mes = 'Março'
    elif mes == '04':
        nome_mes = 'Abril'
    elif mes == '05':
        nome_mes = 'Maio'
    elif mes == '06':
        nome_mes = 'Junho'
    elif mes == '07':
        nome_mes = 'Julho'
    elif mes == '08':
        nome_mes = 'Agosto'
    elif mes == '09':
        nome_mes = 'Setembro'
    elif mes == '10':
        nome_mes = 'Outubro'
    elif mes == '11':
        nome_mes = 'Novembro'
    else:
        nome_mes = 'Dezembro'

    return nome_mes


def scrap_pagina(chrome, txt, txt_num_processos, elem, num_processo_parado):
    try:
        processo = elem.find_element(By.CLASS_NAME, 'processo')
        text_processo = outer_html(processo)

        if not text_processo:
            return False

        # Após os testes substituir o print por txt.write()
        txt.write(f'<P>{text_processo}' + "\n")

        # Pegar os dados do relator
        try:
            relator = elem.find_element(By.CLASS_NAME, 'relator')
        except:
            relator = elem.find_element(By.CLASS_NAME, 'relator')

        text_relator = outer_html(relator)
        txt.write(text_relator + "\n")

        # Pegar a data do despacho
        try:
            despacho = elem.find_elements(
                By.TAG_NAME, 'md-chips-wrap'
                )
        except:
            despacho = elem.find_elements(
                By.TAG_NAME, 'md-chips-wrap'
                )
        # data de despacho
        text_despacho = outer_html(despacho[1])
        data_despacho = text_despacho[-31:-1]
        txt.write(data_despacho + "\n")

        # Pegar os dados dos envolvidos no processo
        try:
            envolvidos = elem.find_element(
                By.CLASS_NAME, 'ng-hide'
                )
        except:
            envolvidos = elem.find_element(
                By.CLASS_NAME, 'ng-hide'
                )
        envolvidos = envolvidos.find_elements(By.CLASS_NAME, 'envolvido')

        for envolvido in envolvidos:
            text_envolvido = outer_html(envolvido)
            txt.write(text_envolvido + "\n")

        try:
            # Função que busca o texto escondido em shadow
            shadow_section = elem.find_element(By.CLASS_NAME, 'shadow')
        except:
            return False

        shadow_root_dict = chrome.execute_script(
            "return arguments[0].shadowRoot", shadow_section
            )
        shadow_root_id = shadow_root_dict['shadow-6066-11e4-a52e-4f735466cecf']

        try:
            shadow_root = WebElement(chrome, shadow_root_id, w3c=True)
        except:
            shadow_root = WebElement(chrome, shadow_root_id, w3c=True)

        # Workarround para pegar a decisão que agora está dentro de uma div
        try:
            decisao = shadow_root.find_element(
                            By.CLASS_NAME, 'P1'
                            )
            texto_decisao = outer_html(decisao)
            txt.write(texto_decisao)
        except:
            pass

        try:
            content_html = shadow_root.find_elements(
                By.TAG_NAME, 'p'
                )
        except:
            content_html = shadow_root.find_elements(
                By.TAG_NAME, 'p'
                )

        for conteudo in content_html:
            # Desvio para corrigir problema de não carregar o HTML
            texto = outer_html(conteudo)
            # try:
            #    html_content = conteudo.get_attribute('outerHTML')
            # except:
            #    html_content = conteudo.get_attribute('outerHTML')
            # soup = BeautifulSoup(html_content, 'html.parser')
            # texto = soup.get_text()

            if len(texto) < 3:
                continue
            
            # Escrever texto raspado no arquivo txt
            txt.write(texto + "\n")
            # try:
            #     txt.write(texto + "\n")
            # except:
            #     for x in texto:
            #         if x == '\u0303' or x == '\u0301' or x == '\x96' or x == '\u0327' or x == '\u0315' \
            #         or x == '\u201f' or x == '\u02da' or x == '\u0300' or x == '\u02c8' or x == '\u2215' \
            #         or x == '\u25aa' or x == '\u2012' or x =='\u202f' or x == '\u0302' or x == '\u030a' \
            #         or x == '\u03b2'or x == '\u27a2':
            #             continue
            #         elif x == '\u2212':
            #             x = '-'
            #         txt.write(x)
        # Alimentar o arquivo como número do processo
        txt_num_processos.write(f'{num_processo_parado}) <P>{text_processo}' + "\n")
        return True
    except Exception as err:
        print(err)
        txt_num_processos.write(f'\nNúmero de Processos = {num_processo_parado +1}\n\n')
        chrome.close()
        txt.close()
        txt_num_processos.close()
        return err

def continuar_parametro():
    url = 'https://digital.stf.jus.br/publico/publicacoes'
    # PATH_DRIVER = 'chromedriver.exe'
    # Apresentar o número de registros encontrados e baixados

    date_hour_start = datetime.today().strftime('%d/%m/%Y %H:%M')
    print('')
    data = input('Escolha a data, do arquivo a ser continuado, no padrão DD/MM/AAAA: ')
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
        print(
            'OPÇÕES DE BUSCA PARA CONTINUAR: \n1 - Publicação \n2 - Divulgação \n3 - Sair do Programa\n')
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

    num_processo_parado = input('\nDigite o número de processos gravados no arquivo Incompleto: ')
    num_processo_parado = int(num_processo_parado)
    print('')
    
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    # options.add_argument("--headless")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')

    # Criando objeto chrome sem precisar ficar baixando a versão atual do chromedriver
    chrome = webdriver.Chrome(
        options=options,
        service=ChromeService(ChromeDriverManager().install())
        )
    chrome.get(url)

    sleep(5)

    # Abrir arquivo
    caminho_arquivo = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}.txt'
    nome_arquivo = f'STFSITE-{ano}.{mes}.{dia}.txt'
    caminho_resumo = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}-Resumo.txt'
    caminho_num_processos = f'C:/sei-dj/stfsite/STFSITE-{ano}.{mes}.{dia}-NumProcessos.txt'

    # Abrindo arquivo para adicionar processos faltantes
    # txt = codecs.open(caminho_arquivo, 'a', errors="ignore")
    txt = open(caminho_arquivo, 'a', errors="ignore")

    # Gerando o arquivo de resumo
    resumo = open(caminho_resumo, 'w')
    first_row = f'STFSITE: {opcao_texto}: {dia}/{mes}/{ano} ARQUIVO: {nome_arquivo}'
    resumo.write(first_row + '\n')

    # Definir a data
    # Chamar função que define a data e escolhe a opção publicação ou divulgação
    set_date(chrome, data, opcao_texto)
    sleep(7)

    # Pegar número total de registros
    registros = outer_html(chrome.find_element(By.CLASS_NAME, 'dataTables_info'))
    num_processos = registros.split(' ')[1]

    range = int(num_processo_parado) / 10
    
    count_page = 1
    count_num_processos = 0
    while count_page <= range:
        count_num_processos += 10
        # Function to press the next button
        chrome.find_element(
            By.XPATH, '//*[@id="conteudo"]/div[3]/md-content/div[1]/dir-pagination-controls/div/div[2]/div[2]/div/a[2]'
            ).click()
        sleep(1.5)
        count_page += 1
    sleep(1)

    processo_seguinte = int(num_processo_parado) % 10
    elementos = chrome.find_elements(By.CLASS_NAME, 'publicacoes')
    

    txt_num_processos = open(caminho_num_processos, 'a')
    for elem in elementos[processo_seguinte:]:
        num_processo_parado += 1
        alimentar_arquivo = scrap_pagina(chrome, txt, txt_num_processos, elem, num_processo_parado)

    print(f'Página {count_page} gravada!')
    count_num_processos += 10

    # Desenvolver lógica para pegar o restante das páginas
    while count_num_processos < int(num_processos):
        proxima_pagina = chrome.find_element(
            By.XPATH, '//*[@id="conteudo"]/div[3]/md-content/div[1]/dir-pagination-controls/div/div[2]/div[2]/div/a[2]'
            )
        proxima_pagina.click()
        sleep(2)
        elementos = chrome.find_elements(By.CLASS_NAME, 'publicacoes')

        for elem in elementos:
            num_processo_parado += 1
            scrap_pagina(chrome, txt, txt_num_processos, elem, num_processo_parado)

        count_page += 1
        print(f'Página {count_page} gravada!')
        count_num_processos += 10

# Adicionar informações no arquivo de Resumo
    date_hour_end = datetime.today().strftime('%d/%m/%Y %H:%M')
    second_row = f'Início: {date_hour_start}h - Término: {date_hour_end}h'
    resumo.write(second_row + '\n')
    resumo.write(f'Total de Processos: Encontrados {num_processos} registros' + '\n')
    resumo.write(f'Processos Baixados: {num_processos}' + '\n')
    resumo.write('Situação: DOWNLOAD OK')

    txt_num_processos.write(f'\nNúmero de Processos = {num_processo_parado}\n\n')

    resumo.close()
    txt.close()
    txt_num_processos.close()
    chrome.close()
    exit()

def set_date(chrome, data, opcao_processo='Divulgação'):
    # Definir a data início
    elem = chrome.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[2]/md-sidenav/md-card[3]/md-card-content/div[1]/div[2]/md-datepicker/div/input'
        )
    elem.send_keys(Keys.CONTROL, 'a')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(data)
    sleep(0.5)

    # Definir a data fim
    elem = chrome.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[2]/md-sidenav/md-card[3]/md-card-content/div[2]/div[2]/md-datepicker/div[1]/input'
        )
    elem.send_keys(Keys.CONTROL, 'a')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(data)

    if opcao_processo == 'Divulgação':
        # Definir opção Divulgação
        elem = chrome.find_element(By.CLASS_NAME, 'md-text')
        elem.click()
        sleep(1)
        elem = chrome.find_element(By.XPATH, '//*[@id="select_option_5"]')
        elem.click()


def avoid_character(character):
    with open('caracteres.txt', 'r') as file:
        texto = file.readlines()

    for caracter in texto:
        caracter = caracter.replace('\n', '')
        
        if character == caracter:
            return True

    return False

