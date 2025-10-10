import pandas as pd
import requests
import json
import time
import os 
import dateparser 

SERPER_API_KEY = "8ffe02f058aad8cd51bf88ee933cdaac9af0e71e"  #mudar e colocar a paga 
SERPER_ENDPOINT = "https://google.serper.dev/news"
NOME_ARQUIVO_CSV = 'v2/noticias_coleta_serper_COMPLETA.csv'
NOME_ARQUIVO_LOG = 'serper/queries_concluidas.txt'

def buscar_noticias_brutas_serper(query_com_and, ano):
    noticias_brutas = []
    tema_simples = query_com_and.replace(' AND ', ' ')
    tema_com_filtro_data = f'{tema_simples} after:{ano}-01-01 before:{ano}-12-31'
    print(f"    [Query Enviada] {tema_com_filtro_data}")
    for page in range(1, 11):
        payload = {"q": tema_com_filtro_data, "page": page, "gl": "br", "hl": "pt"}
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        try:
            response = requests.post(SERPER_ENDPOINT, headers=headers, data=json.dumps(payload))
            response.raise_for_status() 
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"    ERRO CRÍTICO na chamada Serper (Página {page}): {e}")
            return None
        if 'news' not in data or not data['news']:
            print(f"    -> Página {page}: Fim dos resultados encontrados.")
            break 
        
        noticias_encontradas_nesta_pagina = len(data['news'])
        
        for item in data['news']:
            data_texto = item.get('date', None)
            data_formatada = 'Data não disponível'
            
            if data_texto:
                try:
                    data_obj = dateparser.parse(data_texto)
                    if data_obj:
                        data_formatada = data_obj.strftime('%d/%m/%Y')
                except Exception:
                    data_formatada = data_texto

            noticia = {
                'titulo': item.get('title', 'Título não disponível'),
                'link': item.get('link', ''),
                'data_publicacao': data_formatada, 
                'fonte': item.get('source', 'Fonte não disponível')
            }
            noticias_brutas.append(noticia)
            
        print(f"    -> Página {page}: {noticias_encontradas_nesta_pagina} artigos adicionados.")
        time.sleep(1)
    return noticias_brutas


def carregar_queries_concluidas(arquivo_log):
    if not os.path.exists(arquivo_log):
        return set()
    with open(arquivo_log, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def logar_query_concluida(query_id, arquivo_log):
    with open(arquivo_log, 'a', encoding='utf-8') as f:
        f.write(f"{query_id}\n")

def salvar_dados_incrementais(novas_noticias, nome_arquivo):
    if not novas_noticias:
        return
    df = pd.DataFrame(novas_noticias)
    header = not os.path.exists(nome_arquivo)
    df.to_csv(nome_arquivo, mode='a', index=False, header=header, encoding='utf-8-sig')

def gerar_permutacoes_completas(termos_tecnologia, termos_grupo, termos_impacto):
    permutacoes = []
    for t in termos_tecnologia:
        for g in termos_grupo:
            for i in termos_impacto:
                query_amostra = f'{t} AND {g} AND {i}'
                permutacoes.append(query_amostra)
    return permutacoes

if __name__ == '__main__':
    termos_tecnologia = ["reconhecimento facial", "identificacao facial", "deteccao facial", "biometria facial", "autenticacao facial", "sistema de reconhecimento"]
    termos_grupo = ["negro", "negra", "preto", "preta", "pardo", "parda", "afro-brasileiro", "afro-brasileira", "afrodescendente", "movimento negro", "comunidade negra", "população negra", "comunidades marginalizadas", "favelas", "periferia", "comunidade"]
    termos_impacto = ["discriminacao", "racismo", "racista", "injustica", "erro", "engano", "falso positivo", "acusado", "acusada", "acusacao", "vies", "vieses", "prisao", "detencao", "preconceito", "inocente", "injustamente", "preso por engano", "violacao de direitos"]
    ANOS_BASE = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    
    LISTA_DE_QUERIES = gerar_permutacoes_completas(termos_tecnologia, termos_grupo, termos_impacto)
    
    queries_concluidas = carregar_queries_concluidas(NOME_ARQUIVO_LOG)
    print(f"Iniciando/Continuando a busca. {len(queries_concluidas)} buscas já foram concluídas e serão puladas.")
    print("-" * 60)

    for i, query_amostra in enumerate(LISTA_DE_QUERIES):
        for ano in ANOS_BASE:
            query_id = f"{query_amostra} | {ano}"
            
            if query_id in queries_concluidas:
                continue

            print(f"\n--- Executando busca para: '{query_id}' ---")
            
            noticias_coletadas = buscar_noticias_brutas_serper(query_amostra, ano)
            
            if noticias_coletadas is None:
                print("\n!!! A BUSCA FALHOU. PROVAVELMENTE OS CRÉDITOS ACABARAM. ENCERRANDO O SCRIPT. !!!")
                print("Os dados coletados até agora estão salvos.")
                exit() 

            if noticias_coletadas:
                salvar_dados_incrementais(noticias_coletadas, NOME_ARQUIVO_CSV)
                print(f"    -> {len(noticias_coletadas)} artigos salvos em '{NOME_ARQUIVO_CSV}'.")
            
            logar_query_concluida(query_id, NOME_ARQUIVO_LOG)
            
            time.sleep(2)

    print("\nCOLETA DE DADOS CONCLUÍDA COM SUCESSO!")
