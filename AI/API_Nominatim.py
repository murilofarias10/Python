#Autor: Murilo Farias
#Este projeto foi realizado com objetivo de utilizar a API Nominatim gratuitamente e preencher latitudes e longitudes de endereços que 
#havia em uma planilha.

import requests
import openpyxl
from time import sleep

# Caminho para o arquivo Excel original usando raw string para evitar problemas de escape
caminho_arquivo_original = r'C:\Users\MuriloFarias\Desktop\Dados\Teste.xlsx'

# Gerar um novo nome para o arquivo que será salvo com as atualizações
novo_nome_arquivo = caminho_arquivo_original.replace('Teste.xlsx', 'dados_atualizados.xlsx')

# Carregar a planilha do arquivo original
wb = openpyxl.load_workbook(caminho_arquivo_original)
sheet = wb['Dados']  # Acessa a aba chamada 'Dados'

# Função para buscar informações via Nominatim API
def buscar_informacoes_osm(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': endereco,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1  # Solicita detalhes do endereço
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        dados = response.json()
        if dados:
            return dados[0]['lat'], dados[0]['lon']
    return None, None

# Processar os endereços e adicionar latitude e longitude às colunas 'K' e 'L'
for row in range(2, sheet.max_row + 1):  # Ajuste o '2' se sua tabela começar em uma linha diferente
    endereco = f"{sheet[f'G{row}'].value}, {sheet[f'I{row}'].value}"
    lat, lon = buscar_informacoes_osm(endereco)
    sheet[f'K{row}'] = lat or 'Não encontrado'
    sheet[f'L{row}'] = lon or 'Não encontrado'
    print(f"Processado: {endereco} => Lat: {lat}, Lon: {lon}")
    sleep(1)  # Para respeitar os limites da API

# Salvar as modificações em um novo arquivo, mantendo o original sem alterações
wb.save(novo_nome_arquivo)

# Mensagem indicando que o processo foi finalizado e o nome do novo arquivo
print("Processo finalizado. O novo arquivo foi salvo como:", novo_nome_arquivo)

