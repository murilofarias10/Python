#Autor: Murilo Farias
#Este projeto foi realizado com objetivo de utilizar a API Serper com uma conta paga e realizar buscas no google
#de maneira massiva, os dados que seriam utilizados como busca estavam numa planilha e após realizar as raspagem
#era preenchido em outra planilha e salvo automaticamente.

import openpyxl
import requests
import json

# Caminho para o arquivo Excel original e para o novo arquivo
caminho_arquivo_original = r'C:\Users\MuriloFarias\Desktop\Dados\Teste.xlsx'
novo_nome_arquivo = caminho_arquivo_original.replace('Teste.xlsx', 'resultado_atualizado.xlsx')

# Carregar a planilha do arquivo original
wb = openpyxl.load_workbook(caminho_arquivo_original)
sheet = wb['Dados']  # Acessa a aba chamada 'Dados'

# Função para fazer a consulta à API e retornar os dados orgânicos
def consultar_api(endereco):
    url = "https://google.serper.dev/search"
    payload = json.dumps({
      "q": endereco,
      "gl": "br",
      "hl": "pt-br",
      "type": "search",  # Adicionando o tipo de pesquisa
      "engine": "google"  # Adicionando o mecanismo de busca
    })
    headers = {
      'X-API-KEY': 'XX',  # Substitua SuaChaveAPIAqui pela sua chave de API real
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('organic', [])
    else:
        print(f"Erro na consulta API: {response.status_code}")
    return []

# Processar as linhas e atualizar a planilha
for row in range(2, sheet.max_row + 1):
    # Verifica se a primeira célula da coluna J está em branco
    if not sheet['J2'].value:
        print("Coluna J2 está em branco, finalizando as consultas.")
        break
    
    endereco_coluna_g = sheet[f'G{row}'].value or ""
    endereco_coluna_j = sheet[f'J{row}'].value or ""
    endereco_coluna_v = sheet[f'V{row}'].value or ""  # Adicionando a coluna V
    endereco = f"{endereco_coluna_g} {endereco_coluna_j} {endereco_coluna_v}".strip()

    if not endereco:
        print(f"Linha {row} vazia ou incompleta. Pulando.")
        continue

    print(f"Buscando informações para o endereço: {endereco}")

    resultados_organicos = consultar_api(endereco)
    if resultados_organicos:
        # Pegando os resultados nas posições 1 e 2
        for i, resultado in enumerate(resultados_organicos[:2], start=1):
            col_title = chr(ord('K') + (i - 1) * 4)  # K para posição 1, O para posição 2
            col_link = chr(ord('L') + (i - 1) * 4)  # L para posição 1, P para posição 2
            col_snippet = chr(ord('M') + (i - 1) * 4)  # M para posição 1, Q para posição 2
            col_position = chr(ord('N') + (i - 1) * 4)  # N para posição 1, R para posição 2
            
            sheet[f'{col_title}{row}'] = resultado.get('title', 'Não encontrado')
            sheet[f'{col_link}{row}'] = resultado.get('link', 'Não encontrado')
            sheet[f'{col_snippet}{row}'] = resultado.get('snippet', 'Não encontrado')
            sheet[f'{col_position}{row}'] = resultado.get('position', 'Não encontrado')
    else:
        print(f"Nenhum resultado encontrado para: {endereco}")
    
    # Salva após processar cada linha
    wb.save(novo_nome_arquivo)


print(f"Processo finalizado. O novo arquivo foi salvo como: {novo_nome_arquivo}")
