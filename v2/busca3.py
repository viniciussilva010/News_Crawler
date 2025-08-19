import csv
from pygooglenews import GoogleNews
from datetime import datetime

# ------------------------ Função que monta a query (não usada na nova versão, mas mantida) ------------------------
def montar_query_logica(lista_ou):
    """
    Recebe uma lista de listas. Cada sublista representa um grupo AND.
    O retorno é uma string com (A AND B) OR (C AND D) etc.
    """
    grupos_formatados = []
    for grupo in lista_ou:
        termos_and = []
        for termo in grupo:
            if " " in termo:
                termos_and.append(f'"{termo}"')  # Coloca frases entre aspas
            else:
                termos_and.append(termo)
        grupo_formatado = " AND ".join(termos_and)
        grupos_formatados.append(f"({grupo_formatado})")
    
    return " OR ".join(grupos_formatados)

# ------------------------ Função que busca notícias ------------------------
def buscar_noticias(tema, ano, limite=None):
    gn = GoogleNews(lang='pt', country='BR')
    data_inicio = f'{ano}-01-01'
    data_fim = f'{ano}-12-31'

    search = gn.search(tema, from_=data_inicio, to_=data_fim)
    
    noticias = []
    itens_para_processar = search['entries'][:limite] if limite is not None else search['entries']

    for item in itens_para_processar:
        try:
            data_publicacao_dt = datetime.strptime(item.published, '%a, %d %b %Y %H:%M:%S GMT')
            data_formatada = data_publicacao_dt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            data_formatada = ""

        noticia = {
            'titulo': item.title,
            'link': item.link,
            'data_publicacao': data_formatada
        }
        noticias.append(noticia)
        
    return noticias

def salvar_em_csv(noticias, nome_arquivo):

    if not noticias:
        print("Nenhuma notícia encontrada para os critérios definidos.")
        return

    noticias_com_data = [n for n in noticias if n['data_publicacao']]
    noticias_sem_data = [n for n in noticias if not n['data_publicacao']]

    noticias_ordenadas = sorted(noticias_com_data, key=lambda x: x['data_publicacao'], reverse=True)
    
    lista_final = noticias_ordenadas + noticias_sem_data
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['data_publicacao', 'titulo', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(lista_final)
            
    print(f"\nOperação concluída com sucesso!")
    print(f"Total de {len(lista_final)} links salvos no arquivo '{nome_arquivo}'.")

if __name__ == '__main__':
    # --- NOVO: Configuração da query de pesquisa de forma modular ---
    termos_tecnologia = ["reconhecimento facial", "identificacao facial", "deteccao facial", "biometria facial", "autenticacao facial", "sistema de reconhecimento"]
    termos_grupo = ["negro", "negra", "preto", "preta", "pardo", "parda", "afro-brasileiro", "afro-brasileira", "afrodescendente", "movimento negro", "comunidade negra", "população negra", "comunidades marginalizadas"]
    termos_impacto = ["discriminacao", "racismo", "racista", "injustica", "erro", "engano", "falso positivo", "acusado", "acusada", "acusacao", "vies", "vieses", "prisao", "detencao"]

    # Constrói os subgrupos com OR
    query_tecnologia = " OR ".join([f'"{termo}"' for termo in termos_tecnologia])
    query_grupo = " OR ".join([f'"{termo}"' for termo in termos_grupo])
    query_impacto = " OR ".join([f'"{termo}"' for termo in termos_impacto])

    # Combina os subgrupos com AND para formar a query final
    TEMA_PESQUISA = f'({query_tecnologia}) AND ({query_grupo}) AND ({query_impacto})'

    ANOS_PESQUISA = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    LIMITE_POR_ANO = 10000000000

    #nome do arquivo
    nome_do_arquivo = 'noticias_discriminacao_racismo_e_erros_rf.csv'

    print("Iniciando busca de notícias com as seguintes configurações:")
    print(f"  - Tema (query lógica): {TEMA_PESQUISA}")
    print(f"  - Anos: {ANOS_PESQUISA}")
    print(f"  - Limite por ano: {LIMITE_POR_ANO}")
    print("-" * 40)

    todas_as_noticias = []

    for ano in ANOS_PESQUISA:
        print(f"Buscando notícias para o ano de {ano}...")
        noticias_do_ano = buscar_noticias(TEMA_PESQUISA, ano, limite=LIMITE_POR_ANO)
        todas_as_noticias.extend(noticias_do_ano) 
        print(f"  -> {len(noticias_do_ano)} notícias encontradas para {ano}.")

    salvar_em_csv(todas_as_noticias, nome_do_arquivo)
