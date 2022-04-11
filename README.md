# AutomacaoBuscaPrecos

Automação de Busca de Precos no Google Shopping e Buscapé

### Utilidade
O WebScrapping resulta muito util para automatizar tarefas repetitivas e que possivemente consuman muito tempo. Busca de preços provee uma lista de dados para acelerar a compra e venda de um produto, baseado no valor.

### Arquivos do projeto

    buscas.xlsx
    contem uma lista de items que serão pesquisados

    login.txt
    Deve conter os dados de login para enviar o e-mail. Primeira linha com o-mail, segunda linha com a senha.

    pesquisaPreco.py
    Codigo em Python da automação

### Como usar
#### Bibliotecas requeridas
    - pandas
    - selenium
    - yagmail
#### Arquivos
    - Alterar o arquivo login.txt para conter o e-mail e a senha de uma conta gmail, para o envio do e-mail.
    - Alterar o arquivo buscas.xlsx para definir os parametros da busca.
    
#### Obs.
O site de Buscapé muda com certa frecuencia, por isso é possivel que a automação não funcionde ou de algum erro
