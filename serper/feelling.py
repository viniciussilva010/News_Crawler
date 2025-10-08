import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm import tqdm
import os

def analisar_sentimentos_leia(arquivo_csv_entrada, arquivo_csv_saida, arquivo_grafico):
    """
    Realiza a análise de sentimentos usando a biblioteca LeIA (VADER em Português).
    """
    print(f"Lendo o arquivo de dados: {arquivo_csv_entrada}")
    if not os.path.exists(arquivo_csv_entrada):
        print(f"ERRO: O arquivo '{arquivo_csv_entrada}' não foi encontrado.")
        return

    # Baixa o léxico necessário para a análise de sentimentos (apenas na primeira vez)
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("Baixando o léxico VADER (necessário apenas na primeira execução)...")
        nltk.download('vader_lexicon')

    # 1. Carregar os dados
    df = pd.read_csv(arquivo_csv_entrada)
    df.dropna(subset=['titulo'], inplace=True)

    # 2. Inicializar o analisador de sentimentos
    print("Inicializando o analisador de sentimentos LeIA...")
    sia = SentimentIntensityAnalyzer()

    # 3. Analisar o sentimento de cada título
    print(f"Analisando o sentimento de {len(df)} títulos de notícias...")
    
    resultados = []
    for titulo in tqdm(df['titulo'], desc="Analisando títulos"):
        # O método polarity_scores retorna um dicionário com pontuações
        scores = sia.polarity_scores(titulo)
        
        # Classificamos o sentimento com base na pontuação 'compound' (-1 a 1)
        compound_score = scores['compound']
        if compound_score >= 0.05:
            label = 'Positivo'
        elif compound_score <= -0.05:
            label = 'Negativo'
        else:
            label = 'Neutro'
            
        resultados.append({'sentimento': label, 'confianca': compound_score})

    # Adiciona os resultados ao DataFrame
    df_resultados = pd.DataFrame(resultados)
    df['sentimento'] = df_resultados['sentimento']
    df['confianca_sentimento (compound)'] = df_resultados['confianca']

    # 4. Salvar o novo CSV
    print(f"\nSalvando os resultados em '{arquivo_csv_saida}'...")
    df.to_csv(arquivo_csv_saida, index=False, encoding='utf-8-sig')
    print("Arquivo salvo com sucesso.")

    # 5. Gerar o gráfico
    distribuicao = df['sentimento'].value_counts(normalize=True) * 100
    print("\nDistribuição dos Sentimentos:")
    print(distribuicao.round(2).to_string())

    print(f"Gerando o gráfico e salvando como '{arquivo_grafico}'...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    distribuicao.plot(kind='bar', ax=ax, color=['#d9534f', '#5cb85c', '#f0ad4e']) # Cores ajustadas
    ax.set_title('Distribuição de Sentimentos nas Notícias (LeIA/VADER)', fontsize=16, pad=20)
    ax.set_ylabel('Porcentagem (%)', fontsize=12)
    ax.set_xlabel('Sentimento', fontsize=12)
    ax.set_xticklabels(distribuicao.index, rotation=0)
    plt.tight_layout()
    plt.savefig(arquivo_grafico)
    print("Gráfico salvo com sucesso.")

if __name__ == '__main__':
    ARQUIVO_DE_DADOS = 'serper/noticias_coleta_serper_COMPLETA.csv'
    ARQUIVO_DE_SAIDA = 'serper/noticias_com_sentimentos_leia.csv'
    NOME_DO_GRAFICO = 'serper/analise_de_sentimentos_leia.png'
    analisar_sentimentos_leia(ARQUIVO_DE_DADOS, ARQUIVO_DE_SAIDA, NOME_DO_GRAFICO)