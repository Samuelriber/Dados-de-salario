'''
Objetivos Específicos:
    Utilizar as bibliotecas BeautifulSoup, Requests e Selenium para raspagem de dados.
    Manipular e analisar dados utilizando a biblioteca pandas.
    Criar visualizações informativas com a biblioteca matplotlib.
    Desenvolver um aplicativo interativo com a biblioteca Streamlit que apresente os dados de forma clara e envolvente.
    Exportar informações em PDF, utilizando a biblioteca PyPDF.
    Aplicar técnicas de storytelling para tornar a apresentação dos dados mais impactante.
    Publicar o arquivo em um repositório do GitHub e fazer o deploy na Streamlit Cloud. 
'''
import io
import csv
import requests
import pandas as pd
import pdfkit
import streamlit as st
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def get_data(url, cabecalho):
    requisicao = requests.get(url=url, headers=cabecalho, verify=False)
    site = BeautifulSoup(requisicao.text, 'html.parser')
    table = site.find_all('div', class_='col-xl-8 col-lg-8')
    salario_now = []
    salario_old = []
    nome = []
    if table:
        for div in table:
            links = div.find_all('a')
            new_val = div.find_all('tr')
            for link in links:
                nome.append(link.text)
            for tr in new_val:
                tds = tr.find_all('td')
                if len(tds) > 1:
                    salario_old.append(tds[1].text.strip())
                if len(tds) > 2:
                    salario_now.append(tds[2].text.strip())
    dados = {
        'País': nome,
        'Salario antigo': salario_old,
        'Salario Agora': salario_now
    }
    return pd.DataFrame(dados)

def clean_data(df):
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

def create_bar_chart(df):
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.bar(df['País'], df['Salario antigo'].astype(float), label='Salario antigo', color='skyblue')
    ax.bar(df['País'], df['Salario Agora'].astype(float), bottom=df['Salario antigo'].astype(float), label='Salario Agora', color='orange')
    ax.set_ylabel('Salário')
    ax.set_title('Comparação de Salários Antigo e Atual por País')
    ax.legend()
    ax.tick_params(axis='x', rotation=60)
    ax.grid(axis='y')
    ax.bar_label(ax.containers[0], label_type='edge')
    ax.bar_label(ax.containers[1], label_type='edge')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2)
    return fig


def export_to_csv(df):
    # Create a CSV file from the DataFrame
    csv_data = df.to_csv(index=False)
    
    st.markdown("### Download arquivo em CSV (Excel)")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="output.csv",
        mime="text/csv"
    )

    

   
    
        
        
        
def main():
    url = 'https://pt.tradingeconomics.com/country-list/minimum-wages?continent=europe'
    cabecalho = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    df = get_data(url, cabecalho)
    df = clean_data(df)
    fig = create_bar_chart(df)
    st.title('Exemplo de Gráfico de Barras com Streamlit e Matplotlib')
    st.write("Dados:")
    st.write(df)
    st.pyplot(fig)
    export_to_csv(df)
    
main()