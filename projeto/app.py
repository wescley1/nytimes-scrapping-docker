"""
Created on Tue Mar  4 11:23:53 2025

@author: wescley
"""

import os
from dotenv import load_dotenv
import time
import pandas as pd
import requests
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse


##############################################################################
######################## DEFINIÇÕES DE FNUNÇÕES ##############################
##############################################################################

# Função para extrair a extensão do arquivo
def extrair_extensao(url):
    # Usar a extensão da URL ou conteúdo do tipo MIME se a URL não tiver extensão
    ext = os.path.splitext(urlparse(url).path)[1]
    if not ext:
        return ".jpg"  # Ou qualquer tipo padrão (ex: '.png')
    return ext

#clica no
def elementos_iniciais():
    #busca elemento de accept all cookies e clica para fechar
    
    acceptAll_button =  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='fides-banner-button fides-banner-button-primary fides-accept-all-button']")))
    acceptAll_button.click()
    time.sleep(1)    
    
    #busca elemento de continue do 'weve uptated our terms' e clica em continuar
    continue_button = driver.find_element(By.CLASS_NAME, "css-j07ljx")
    continue_button.click()
    time.sleep(1)
    
def aplicar_filtros(wait, sections, sorting, month):
    # Encontre o checkbox da categoria e marque
    # Busca elemento Section
   
    # Clique no botão "Section" para abrir os filtros
    section_button = driver.find_element(By.XPATH, "//button[contains(@class,'css-xis2i3')]")
    section_button.click()        
    
    for categoria in sections:
        # Localize e clique no checkbox "Sports"
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@value,'"+categoria+"')]")))
        checkbox.click()
        
    
    # Clique no botão "Section" para abrir os filtros
    section_button = driver.find_element(By.XPATH, "//button[contains(@class,'popup-visible css-xis2i3')]")
    section_button.click()     
    
    time.sleep(1)
    
    ####### Ordena por mais recentes
    
    dropdown = driver.find_element(By.XPATH, "//select[@class='css-1asernv']")
    select = Select(dropdown)

    # Seleciona pelo valor da opção
    select.select_by_value(sorting)
    
    ############### pega os meses definidos
    ##calcula a data inicial como sendo o primeiro dia de MONTHS atrás.
    # por exemplo, hoje é dia 28/02/2025. se a variavel MONTHS for 2, pega o primeiro dia de janeiro.
    #caso especial de month=0
    if month == 0:
        month = 1
    dataHoje = datetime.today()
    dataInicial = dataHoje - relativedelta(months=month-1)
    dataInicial = dataInicial.replace(day=1)
    
    dateRange_button = driver.find_element(By.XPATH,"//button[contains(@class,'css-1ftrdcd')]")
    dateRange_button.click()    
    
    specificDates_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@value,'Specific Dates')]")))
    specificDates_button.click()
    
    startDate_input = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[contains(@aria-label,'start date')]")))
    startDate_input.send_keys(dataInicial.strftime("%m/%d/%Y"))
    
    endDate_input = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[contains(@aria-label,'end date')]")))
    endDate_input.send_keys(dataHoje.strftime("%m/%d/%Y"))
    endDate_input.send_keys(Keys.RETURN)
    
    
    
def extrair_imagem(img_element):
    # Verificar se existe a imagem
    if img_element:
        # Obter o URL da imagem
        imagem_url = img_element.get_attribute("src")
        
        # Baixar a imagem
        if imagem_url:
            print(f"Baixando imagem de: {imagem_url}")
            response = requests.get(imagem_url)
            
            # Salvar a imagem no diretório local
            if response.status_code == 200:
                imagem_nome = re.sub(r'[<>:"/\\|?*]', '_', imagem_url.split("/")[-1])  # Nome da imagem. Remove caracteres que impede o arquivo de ser salvo
                imagem_nome += ".jpg"
                path_imagem = os.path.join(IMAGENS_DIR, imagem_nome)                           
                    
                with open(path_imagem, 'wb') as f:
                    f.write(response.content)
                print(f"Imagem salva como: {imagem_nome}")
                imagem = path_imagem
            else:
                print(f"Falha ao baixar a imagem de {imagem_url}")
                imagem = "Nao foi possível fazer download da imagem"
                
    return imagem
    
def possui_dinheiro(titulo, descricao):
    encontrouOcorrencia = False
    
    padrao = r'(\$|US\$)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?|\d+\s*dólars'
    
    encontrouOcorrencia = bool(re.findall(padrao, titulo, re.IGNORECASE)) or bool(re.findall(padrao, descricao, re.IGNORECASE))
    
    return encontrouOcorrencia
        
def contarOcorrencias(pesquisa, titulo, descricao):
    # Criar um padrão de regex para a palavra, ignorando maiúsculas/minúsculas e considerando palavras inteiras
    padrao = rf'\b{re.escape(pesquisa)}\b'
    
    # Contar ocorrências no título e na descrição
    ocorrencias_titulo = len(re.findall(padrao, titulo, re.IGNORECASE))
    ocorrencias_descricao = len(re.findall(padrao, descricao, re.IGNORECASE))
    
    # Retornar a soma total de ocorrências
    return ocorrencias_titulo + ocorrencias_descricao
    
    

def search_news():
    """Executa a pesquisa no NY Times e retorna os artigos encontrados."""
    driver.get("https://www.nytimes.com/")    
        
    
    try:
        elementos_iniciais()
    except:
        print("Nao foram encontrados elementos iniciais")

    # Clicar no botão de pesquisa
    search_button = driver.find_element(By.XPATH, "//button[contains(@class,'css-tkwi90 e1iflr850')]")
    search_button.click()
    time.sleep(2)


    # Inserir a frase de pesquisa
    search_box = driver.find_element(By.NAME, "query")
    search_box.send_keys(SEARCH_PHRASE)
    search_box.send_keys(Keys.RETURN)
    wait = WebDriverWait(driver, 10)
    
    aplicar_filtros(wait, CATEGORIES, SORTING, MONTHS)
    
    time.sleep(3)

    # Coletar as notícias
    articles = driver.find_elements(By.CLASS_NAME, "css-1l4w6pd")
    news_data = []

    for article in articles:
        try:
            title_element = article.find_element(By.TAG_NAME, "h4")
            title = title_element.text

            link_element = article.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")

            #informações de data
            try:
                date_element = article.find_element(By.CSS_SELECTOR, "span.css-y0k07m")
                date = date_element.text
            except:
                date = "Sem data"

            #informação da descrição
            try:
                description_element = article.find_element(By.CSS_SELECTOR, "p.css-e5tzus")
                description = description_element.text
            except:
                description = "Sem descrição"
                
            #informação da imagem    
            try:
                imagem_element = article.find_element(By.XPATH, ".//img")   
                imagem = extrair_imagem(imagem_element)
            except:                
                imagem = "Sem imagem"
                
            #verifica se possui dinheiro
            try:
                possuiDinheiro = possui_dinheiro(title, description)
            except:
                possuiDinheiro = False
                
            #conta ocorrencias da busca
            try:
                ocorrenciasBusca = contarOcorrencias(SEARCH_PHRASE, title, description)
                if ocorrenciasBusca == 0:
                    ocorrenciasBusca = "Não foi encontrada ocorrências."
            except:
                ocorrenciasBusca = "Sem ocorrências."    
                

            news_data.append({"Título": title, "Data": date, "Descrição": description, "Possui Dinheiro": str(possuiDinheiro), "Ocorrencias da busca":ocorrenciasBusca, "Imagem": imagem, "Link": link})

        except Exception as e:
            print(f"Erro ao extrair artigo: {e}")

    return news_data

################################################################
################ CONFIGURAÇÕES INICIAIS ########################
################################################################


# Carregar as variáveis do .env
print("Lendo as variáveis de ambiente.")
try:
    load_dotenv()
except Exception as e:
    print(f"Houve erro ao ler as variaveis de ambiente. Detalhes do erro: {e}")
    raise SystemExit(f"Houve erro ao ler as variaveis de ambiente. Detalhes do erro: {e}")

# Ler as variáveis
SEARCH_PHRASE = os.getenv("SEARCH_PHRASE", "")
CATEGORIES = os.getenv("CATEGORIES", "").split(",")  # Transforma em lista
MONTHS = int(os.getenv("MONTHS", "1"))  # Converte para inteiro
SORTING = os.getenv("SORTING","") #Pega tipo de ordenação

print("Variáveis lidas com sucesso.")

# Exibir para teste
print(f"Frase de pesquisa: {SEARCH_PHRASE}")
print(f"Categorias: {CATEGORIES}")
print(f"Meses: {MONTHS}")
print(f"Ordenacao: {SORTING}")

# Configurar o Selenium
print("Iniciando configurações do selenium")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920x1080")

service = Service("/usr/bin/chromedriver") #utiliza o chromedriver instalado via apt-get.
driver = webdriver.Chrome(service=service, options=options)
print("Driver iniciado com sucesso")

RESULTADOS_DIR = os.path.join("resultados") #nome do diretorio onde será salvo os resultados
if not os.path.exists(RESULTADOS_DIR):
    os.makedirs(RESULTADOS_DIR)
    print("Diretório de resultados criado com sucesso")

IMAGENS_DIR = os.path.join(RESULTADOS_DIR,"imagens")
if not os.path.exists(IMAGENS_DIR):
    os.makedirs(IMAGENS_DIR)
    print(f"Diretório de imagens criado com sucesso!")

# Executar a pesquisa
print("Executando busca no site")
try:
    news = search_news()
except Exception as e:
    print(f"Ocorreu algum erro durante execução do script. Detalhes do erro: {e}")

driver.quit()

# Criar DataFrame e salvar os resultados
df = pd.DataFrame(news)
df.to_excel(os.path.join(RESULTADOS_DIR, "news_results.xlsx"), index=False)
print(f"Extração concluída! Resultados salvos em {RESULTADOS_DIR}/news_results.xlsx")

print("Fim da execução.")
