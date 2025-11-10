# Filtragem e Limpeza do Corpus
O arquivo de dados brutos (noticias_coleta_serper_COMPLETA.csv) foi gerado a partir de uma busca ampla, o que resultou na coleta de 8.582 notícias. No entanto, essa abordagem também capturou "ruído" (artigos em que os termos de busca apareciam, mas fora do contexto da pesquisa).
O objetivo desta fase foi limpar o corpus, mantendo apenas os títulos relevantes.

# Abordagem: Filtragem por Similaridade Semântica
Para garantir a relevância do corpus, implementamos um filtro de IA (NLP) para analisar o significado de cada título, em vez de depender apenas de palavras-chave exatas.
* Ferramenta: SentenceTransformer (utilizando o modelo paraphrase-multilingual-MiniLM-L12-v2).
* Vetores-Conceito: Definimos três conceitos centrais para a pesquisa, representados por listas de palavras-chave:
  1. Tecnologia: Termos como "reconhecimento facial", "algoritmo", "IA".
  2. Grupo Social: Termos como "negro", "população negra", "pele escura".
  3. Impacto: Termos como "racismo", "erro", "vieses", "prisao".

* Lógica de Relevância (Regra "2 de 3"): Um título foi classificado como Relevante se seu significado fosse semanticamente similar (acima de um limite) a pelo menos dois dos três vetores-conceito (ex: Tecnologia + Grupo, ou Tecnologia + Impacto).
# Calibração do Limite de Similaridade (Threshold)
A etapa mais crucial foi definir o limite (a "nota de corte" ou "média") para a similaridade.

Teste 1 (Limite = 0.50): Este valor se mostrou muito restritivo. Ele capturou apenas 2.525 (29,42%) dos títulos. Uma análise manual mostrou que ele estava descartando muitos artigos relevantes que tinham pontuações ligeiramente abaixo de 0.50.

Teste 2 (Limite = 0.40): Ao reduzir o limite, encontramos o ponto de equilíbrio ideal. O filtro foi capaz de classificar corretamente títulos mais complexos (ex: Google conserta seu algoritmo “racista”) e capturou 5.122 (59,68%) dos títulos. Este ajuste removeu com sucesso 40,32% do ruído, retendo o núcleo de artigos pertinentes.

**Resultado Final:**
O resultado desta fase é o arquivo noticias_corpus_filtrado_semantico_2.csv. Este é o corpus de dados final e limpo, que serve como base para todas as análises subsequentes (temporal, de sentimentos, etc.)
