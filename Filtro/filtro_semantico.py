import pandas as pd
import os
import torch 
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA = 'serper/noticias_coleta_serper_COMPLETA.csv'
ARQUIVO_SAIDA_COMPLETO = 'limpatudo/noticias_analise_semantica2.csv'
ARQUIVO_SAIDA_FILTRADO = 'limpatudo/noticias_corpus_filtrado_semantico2.csv'

# A "MÉDIA" (NOTA DE CORTE):
# Esta é a pontuação mínima para considerar um título "similar" a um conceito.

SIMILARITY_THRESHOLD = 0.40

termos_tecnologia = [
    "reconhecimento facial", "identificacao facial", "deteccao facial", 
    "biometria facial", "autenticacao facial", "sistema de reconhecimento",
    "algoritmo", "algoritmos", "inteligência artificial", "ia"
]
termos_grupo = [
    "negro", "negra", "pretos", "preta", "pardo", "parda", "afro-brasileiro", 
    "afro-brasileira", "afrodescendente", "movimento negro", "comunidade negra", 
    "população negra", "comunidades marginalizadas", "favelas", "periferia", "comunidade",
    "pele escura", "pele negra", "pessoas negras"
]
termos_impacto = [
    "discriminacao", "racismo", "racista", "racistas", "injustica", "erro", "engano", 
    "falso positivo", "acusado", "acusada", "acusacao", "vies", "vieses", "prisao", 
    "detencao", "preconceito", "inocente", "injustamente", "preso por engano", 
    "violacao de direitos", "preso", "presa", "presos", "presas"
]

def filtrar_por_semantica(arquivo_entrada, arquivo_saida_completo, arquivo_saida_filtrado):
    print(f"Lendo o arquivo de dados: {arquivo_entrada}...")
    if not os.path.exists(arquivo_entrada):
        print(f"ERRO: O arquivo '{arquivo_entrada}' não foi encontrado.")
        return
        
    df = pd.read_csv(arquivo_entrada)
    df.dropna(subset=['titulo'], inplace=True)
    titulos = df['titulo'].tolist()

    print("Carregando modelo Sentence Transformer")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    print("Pré-calculando embeddings dos vetores de palavras-chave...")
    embeddings_tech = model.encode(termos_tecnologia, convert_to_tensor=True)
    embeddings_group = model.encode(termos_grupo, convert_to_tensor=True)
    embeddings_impact = model.encode(termos_impacto, convert_to_tensor=True)

    print(f"Codificando {len(titulos)} títulos (isso pode levar vários minutos)...")
    embeddings_titulos = model.encode(titulos, convert_to_tensor=True, show_progress_bar=True)

    print("Calculando similaridade dos títulos com os vetores...")
    # Compara todos os títulos com todos os termos de tecnologia
    sim_matrix_tech = util.cos_sim(embeddings_titulos, embeddings_tech)
    # Compara todos os títulos com todos os termos de grupo
    sim_matrix_group = util.cos_sim(embeddings_titulos, embeddings_group)
    # Compara todos os títulos com todos os termos de impacto
    sim_matrix_impact = util.cos_sim(embeddings_titulos, embeddings_impact)

    # 6. Encontrar a similaridade MÁXIMA para cada título contra cada vetor
    # Para cada título, pegamos a maior pontuação que ele teve com qualquer palavra do vetor
    max_sim_tech = sim_matrix_tech.max(dim=1).values
    max_sim_group = sim_matrix_group.max(dim=1).values
    max_sim_impact = sim_matrix_impact.max(dim=1).values

    # Adiciona os scores ao DataFrame para análise
    df['sim_tecnologia'] = max_sim_tech.cpu().numpy() # .cpu().numpy() converte de tensor para lista
    df['sim_grupo'] = max_sim_group.cpu().numpy()
    df['sim_impacto'] = max_sim_impact.cpu().numpy()

    # 7. Aplicar a regra do "Threshold"
    tem_tech = max_sim_tech > SIMILARITY_THRESHOLD
    tem_group = max_sim_group > SIMILARITY_THRESHOLD
    tem_impact = max_sim_impact > SIMILARITY_THRESHOLD

    # 8. Aplicar a Lógica Flexível (2 de 3)
    # Soma os booleanos (True=1, False=0) e verifica se o total é >= 2
    df['relevante_semantico'] = (tem_tech.int() + tem_group.int() + tem_impact.int()) >= 2

    df.to_csv(arquivo_saida_completo, index=False, encoding='utf-8-sig')
    print(f"Arquivo completo com a análise semântica salvo em: '{arquivo_saida_completo}'")
    
    df_filtrado = df[df['relevante_semantico'] == True]
    df_filtrado.to_csv(arquivo_saida_filtrado, index=False, encoding='utf-8-sig')
    print(f"Arquivo filtrado (semântico) salvo em: '{arquivo_saida_filtrado}'")

    print("\n--- Resumo da Filtragem Semântica (V3) ---")
    print(f"Limite de Similaridade (Média/Corte): {SIMILARITY_THRESHOLD}")
    print(f"Total de títulos analisados: {len(df)}")
    print(f"Total de títulos relevantes (regra 2 de 3): {len(df_filtrado)}")
    print(f"Total de títulos irrelevantes: {len(df) - len(df_filtrado)}")

if __name__ == '__main__':
    filtrar_por_semantica(ARQUIVO_ENTRADA, ARQUIVO_SAIDA_COMPLETO, ARQUIVO_SAIDA_FILTRADO)
