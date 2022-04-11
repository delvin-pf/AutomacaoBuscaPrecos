# ## Projeto Automação Web - Busca de Preços

# Resumo do objetivo:
# Lê uma base de dados com produtos e faz a pesquisa no Google Shopping e Buscapé. Cria um arquivo excel e envia os resultados da busca por emai


def pesquisarGoogle(driver, produto, termosBan, precoMin, precoMax):
    '''
    Busca no site do buscapé pelo produto.
    webdriver instance, string, string, float, float --> list
    Argumentos:
        driver: instancia do webdriver
        produto: nome do produto a ser pesquisado
        termosBan: termo que não deve conter a busca do produto
        precoMin: preço minimo do produto
        precoMax: preço maximo do produto
    Retorno:
        lista de tuplas contendo nome, preço e link dos resultados da busca
    '''
    driver.get('https://www.google.com.br/')
    driver.find_element(By.CLASS_NAME, 'gLFyf').send_keys(produto + Keys.ENTER)
    
    elemento = driver.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for item in elemento:
        if 'Shopping' in item.text:
            item.click()
            break
            
    listaResultados = driver.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')
    listaOfertas = []
    for resultado in listaResultados:
        nome = resultado.find_element(By.CLASS_NAME, 'Xjkr3b').text
        nomeAprovado = verificarNome(nome, produto, termosBan)
             
        if nomeAprovado:
            preco = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
            precoAprovado = verificarPreco(preco, precoMin, precoMax)
           
            if precoAprovado:
                elemLink = resultado.find_element(By.CLASS_NAME, 'aULzUe')
                elemPai = elemLink.find_element(By.XPATH, '..')
                link = elemPai.get_attribute('href')
                listaOfertas.append((nome, preco, link))
    return listaOfertas

def pesquisarBuscape(driver, produto, termosBan, precoMin, precoMax):
    '''
    Busca no site do buscapé pelo produto.
    (webdriver instance, string, string, float, float) --> list
    Argumentos:
        driver: instancia do webdriver
        produto: nome do produto a ser pesquisado
        termosBan: termo que não deve conter a busca do produto
        precoMin: preço minimo do produto
        precoMax: preço maximo do produto
    Retorno:
        lista de tuplas contendo nome, preço e link dos resultados da busca
    '''
    driver.get('https://www.buscape.com.br/')
    driver.find_element(By.CLASS_NAME, 'AutoCompleteStyle_input__FInnF').send_keys(produto + Keys.ENTER)
    # selecionar um elemento unico na pagina (filtro de orden)
    WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'FormGroup_formGroup__label__S4sFy')))
    
    listaResultados = driver.find_elements(By.CLASS_NAME, 'Cell_Content__fT5st')

    listaOfertas = []
    for resultado in listaResultados:
        nome = resultado.get_attribute('title')
        nomeAprovado = verificarNome(nome, produto, termosBan)

        if nomeAprovado:
            preco =  resultado.find_element(By.CLASS_NAME, 'CellPrice_MainValue__JXsj_').text
            precoAprovado = verificarPreco(preco, precoMin, precoMax)

            if precoAprovado:
                link = resultado.get_attribute('href')
                listaOfertas.append((nome, preco, link))
    return listaOfertas

def verificarNome(nome, produto, termosBan):
    '''
    Retorna True se o nome resultado tem todas as palavras chaves e não tem termos banidos. Caso contrario, retorna False
    string, string, string --> boolean
    '''
    nome = nome.lower()
    listaBanidos = termosBan.split(' ')
    listaAprovados = produto.split(' ')
    aprovadoA = [True if palavra in nome else False for palavra in listaAprovados]
    aprovadoB = [True if palavra not in nome else False for palavra in listaBanidos]
    if not False in aprovadoA and not False in aprovadoB:
        return True
    else:
        return False

def verificarPreco(preco, precoMin, precoMax):
    '''
    Retorna True se o preço do resultado está entre o preço maximo e minimo. Caso contrario, retorna False
    string, float, float --> boolean
    '''
    try:
        preco = preco.replace('R$ ', '').replace('.', '').replace(',', '.')
        preco = float(preco)
        if precoMin <= preco <= precoMax:
            return True
        else:
            return False
    except:
        return False
    
# iniciando o codigo

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

produtos = pd.read_excel('buscas.xlsx') # arquivo que contem os parametros da busca
ofertas_df = pd.DataFrame()

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

for i in produtos.index:
    produto = produtos.loc[i, 'Nome']
    termosBan = produtos.loc[i, 'Termos banidos']
    precoMin = produtos.loc[i, 'Preço mínimo']
    precoMax = produtos.loc[i, 'Preço máximo']
    
    listaProdutosGoogle = pesquisarGoogle(driver, produto, termosBan, precoMin, precoMax)
    if listaProdutosGoogle:
        ofertasGoogle = pd.DataFrame(listaProdutosGoogle, columns=['Produto', 'Preço', 'Link'])
        ofertas_df = ofertas_df.append(ofertasGoogle)
    else:
        ofertasGoogle = None
        
    listaProdutosBuscape = pesquisarBuscape(driver, produto, termosBan, precoMin, precoMax)
    if listaProdutosBuscape:
        ofertasBuscape = pd.DataFrame(listaProdutosBuscape, columns=['Produto', 'Preço', 'Link'])
        ofertas_df = ofertas_df.append(ofertasBuscape)
    else:
        ofertasBuscape = None

driver.quit()

ofertas_df = ofertas_df.reset_index(drop=True)
ofertas_df.to_excel('Ofertas.xlsx', index=False)

if len(ofertas_df.index) > 0: 
    import yagmail
    
    with open('login.txt') as login: # arquivo txt contendo o login a senha da conta gmail
        login, senha = login.readlines()  # lendo 1 linha com login e segunda linha com senha
        
    corpo = f'''
    <p>Olá,</p>
    <p>Estes foram os resultados das buscas de hoje. Tambem estão em anexo</p>
    {ofertas_df.to_html(index=False)}   
    <p> Att.,</p>
    <p>Automação Python</p>
    '''
    corpo  = corpo.replace('\n', '')
    yag = yagmail.SMTP(login, senha)
    yag.send(
        to='email-de-exemplo@gmail.com', #e-mail de destino
        subject='Pesquisa de preços',
        contents = corpo,
        )

