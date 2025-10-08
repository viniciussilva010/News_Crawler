import pandas as pd
import requests
import json
import time
import os 


SERPER_API_KEY = "8ffe02f058aad8cd51bf88ee933cdaac9af0e71e" 
SERPER_ENDPOINT = "https://google.serper.dev/news"
NOME_ARQUIVO_CSV = 'noticias_coleta_serper_COMPLETA2.csv'
NOME_ARQUIVO_LOG = 'queries_concluidas.txt'

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
            # NOVO: Retorna None em caso de erro para sinalizar que a busca falhou
            return None
        if 'news' not in data or not data['news']:
            print(f"    -> Página {page}: Fim dos resultados encontrados.")
            break 
        noticias_encontradas_nesta_pagina = len(data['news'])
        for item in data['news']:
            noticia = {
                'titulo': item.get('title', 'Título não disponível'),
                'link': item.get('link', ''),
                'data_publicacao': item.get('date', 'Data não disponível'),
                'fonte': item.get('source', 'Fonte não disponível')
            }
            noticias_brutas.append(noticia)
        print(f"    -> Página {page}: {noticias_encontradas_nesta_pagina} artigos adicionados.")
        time.sleep(1)
    return noticias_brutas

# Função para carregar as queries já concluídas
def carregar_queries_concluidas(arquivo_log):
    if not os.path.exists(arquivo_log):
        return set()
    with open(arquivo_log, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

# Função para salvar uma query no log
def logar_query_concluida(query_id, arquivo_log):
    with open(arquivo_log, 'a', encoding='utf-8') as f:
        f.write(f"{query_id}\n")

# Função para salvar dados de forma incremental
def salvar_dados_incrementais(novas_noticias, nome_arquivo):
    if not novas_noticias:
        return
    df = pd.DataFrame(novas_noticias)
    header = not os.path.exists(nome_arquivo)
    df.to_csv(nome_arquivo, mode='a', index=False, header=header, encoding='utf-8-sig')


def gerar_permutacoes_completas(termos_tec, termos_grupo, termos_impacto):
    permutacoes = []
    for t in termos_tec:
        for g in termos_grupo:
            for i in termos_impacto:
                query_amostra = f'{t} AND {g} AND {i}'
                permutacoes.append(query_amostra)
    return permutacoes


if __name__ == '__main__':
    
    termos_tecnologia = ["reconhecimento facial", "identificacao facial", "deteccao facial", "biometria facial", "autenticacao facial", "sistema de reconhecimento"]
    termos_grupo = ["negro", "negra", "preto", "preta", "pardo", "parda", "afro-brasileiro", "afro-brasileira", "afrodescendente", "movimento negro", "comunidade negra", "população negra", "comunidades marginalizadas", "favelas", "periferia", "comunidade"]
    termos_impacto = ["discriminacao", "racismo", "racista", "injustica", "erro", "engano", "falso positivo", "acusado", "acusada", "acusacao", "vies", "vieses", "prisao", "detencao", "preconceito", "inocente", "injustamente", "preso por engano", "violacao de direitos"]
    ANOS_BASE = [2014, 2015, 2016, 2017] # começa em 2010 e vai ate 2024, ja fiz de 2018 ate 2024 faltando 2010-2017
    
    LISTA_DE_QUERIES = gerar_permutacoes_completas(termos_tecnologia, termos_grupo, termos_impacto)
    
    
    queries_concluidas = carregar_queries_concluidas(NOME_ARQUIVO_LOG)
    print(f"Iniciando/Continuando a busca. {len(queries_concluidas)} buscas já foram concluídas e serão puladas.")
    print("-" * 60)

    for i, query_amostra in enumerate(LISTA_DE_QUERIES):
        for ano in ANOS_BASE:
            query_id = f"{query_amostra} | {ano}"
            
            # Pula a busca se ela já estiver no log
            if query_id in queries_concluidas:
                continue

            print(f"\n--- Executando busca para: '{query_id}' ---")
            
            noticias_coletadas = buscar_noticias_brutas_serper(query_amostra, ano)
            
            # Verifica se a busca falhou (ex: falta de créditos)
            if noticias_coletadas is None:
                print("\n!!! A BUSCA FALHOU. PROVAVELMENTE OS CRÉDITOS ACABARAM. ENCERRANDO O SCRIPT. !!!")
                print("Os dados coletados até agora estão salvos.")
                exit() 

            if noticias_coletadas:
                salvar_dados_incrementais(noticias_coletadas, NOME_ARQUIVO_CSV)
                print(f"  -> {len(noticias_coletadas)} artigos salvos em '{NOME_ARQUIVO_CSV}'.")
            
            # Loga a busca como concluída
            logar_query_concluida(query_id, NOME_ARQUIVO_LOG)
            
            time.sleep(2)

    print("\nCOLETA DE DADOS CONCLUÍDA COM SUCESSO!")
