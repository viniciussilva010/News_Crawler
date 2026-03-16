import pandas as pd
import os

ARQUIVO_ENTRADA = 'similaridade/noticias_coleta_serper_COMPLETA1.csv'
ARQUIVO_SAIDA = 'filtragem/ranking_links_detalhado.csv'

def contar_links_com_detalhes():
    print("\n" + "="*50)
    print("📊 INICIANDO CONTAGEM E EXTRAÇÃO DE DETALHES")
    print("="*50 + "\n")

    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"ERRO: O arquivo '{ARQUIVO_ENTRADA}' não foi encontrado.")
        return

    df = pd.read_csv(ARQUIVO_ENTRADA)
    df.dropna(subset=['link'], inplace=True)

    colunas_disponiveis = df.columns.tolist()
    agg_dict = {'link': 'count'}
    
    if 'titulo' in colunas_disponiveis:
        agg_dict['titulo'] = 'first'
    if 'fonte' in colunas_disponiveis:
        agg_dict['fonte'] = 'first'

    agrupado = df.groupby('link').agg(agg_dict).rename(columns={'link': 'quantidade_aparicoes'}).reset_index()

    agrupado_ordenado = agrupado.sort_values(by='quantidade_aparicoes', ascending=True)

    ordem_colunas = ['titulo', 'fonte', 'quantidade_aparicoes', 'link']
    colunas_finais = [col for col in ordem_colunas if col in agrupado_ordenado.columns]
    agrupado_ordenado = agrupado_ordenado[colunas_finais]

    agrupado_ordenado.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')

    print("\n" + "="*50)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*50)
    print(f"Total de links ÚNICOS encontrados: {len(agrupado_ordenado)}")
    print(f"O seu relatório completo foi salvo em: {ARQUIVO_SAIDA}")

if __name__ == '__main__':
    contar_links_com_detalhes()