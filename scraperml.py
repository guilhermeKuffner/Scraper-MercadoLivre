

from os import execl
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pandas as pd

url='https://lista.mercadolivre.com.br/rodas-de-skate#D[A:rodas%20de%20skate,L:undefined]'
wb = Workbook()
planilha = wb.worksheets[0]
planilha['A1'] ="Produto"
planilha['B1'] ="Preço"
i=1

site = requests.get(url)
soup = BeautifulSoup(site.content,'html.parser')
tabela=soup.find('ol', attrs={'class':'ui-search-layout ui-search-layout--stack'} )
produto = tabela.find('li',attrs={'class':'ui-search-layout__item'})
oi=soup.find('li',attrs={'class':'andes-pagination__page-count'})
def string_to_int(s):
    try:
        temp = int(eval(str(s)))
        if type(temp) == int:
            return temp
    except:
        return
numpg = string_to_int(oi.text.strip('de '))
x=0
while x<numpg:
    proxpg = soup.find('a',attrs={'class':'andes-pagination__link ui-search-link'})
    next = proxpg['href']
    
    site = requests.get(next)
    soup = BeautifulSoup(site.content,'html.parser')
    tabela=soup.find('ol', attrs={'class':'ui-search-layout ui-search-layout--stack'} )
    produto = tabela.find('li',attrs={'class':'ui-search-layout__item'})
    print("x =",x)  

    for produto in tabela.find_all('li',attrs={'class':'ui-search-layout__item'}):
       
        i=i+1
        print("i =",i)    
        b = str(i)
        nomeprod = produto.find('div',attrs={'class':'ui-search-item__group ui-search-item__group--title'})
        precoprod = produto.find('span',attrs={'class':'price-tag-fraction'})
        hyperlink= produto.find('a',attrs={'class':'ui-search-item__group__element ui-search-link'})
        prodUrl=hyperlink['href']
        planilha['A'+b] = nomeprod.text
        planilha['B'+b] ='R$'+ precoprod.text
        link = requests.get(prodUrl)
        soup2= BeautifulSoup(link.content,'html.parser')
        reput = soup2.find('ul', attrs={'class':'ui-thermometer'} )
        planilha['C'+b] =reput['value']
    x=x+1
   

#andes-pagination__page-count



        

    
wb.save("E:\estudo\Produtos.xlsx")
ht= pd.read_excel("E:\estudo\Produtos.xlsx")
arq = open ("mercadoLivre.html","w")
arq.write(ht.to_html())




