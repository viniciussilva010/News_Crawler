import pandas as pd

def remover_duplicatas_csv(nome_arquivo_entrada, nome_arquivo_saida):
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv(nome_arquivo_entrada)

        # Remove duplicatas com base nas colunas 'titulo' e 'link'
        df_sem_duplicatas = df.drop_duplicates(subset=['titulo', 'link'], keep='first')

        # Salva o DataFrame sem duplicatas em um novo arquivo
        df_sem_duplicatas.to_csv(nome_arquivo_saida, index=False)

        print(f"Total de {len(df)} notícias originais.")
        print(f"Total de {len(df_sem_duplicatas)} notícias únicas salvas em '{nome_arquivo_saida}'.")
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo_entrada}' não foi encontrado.")

if __name__ == '__main__':
    # Exemplo de uso:
    arquivo_original = 'noticias_discriminacao_racismo_e_erros_rf.csv' # Nome do arquivo que contém duplicatas
    arquivo_limpo = 'noticias_discriminacao_racismo_e_erros_rf_limpo.csv' # Nome do novo arquivo sem duplicatas
    remover_duplicatas_csv(arquivo_original, arquivo_limpo)