# Busca Automatizada de Notícias com pygooglenews

Este projeto em Python realiza uma busca automatizada por notícias utilizando a biblioteca `pygooglenews`, filtrando os resultados com base em uma consulta lógica e salvando-os em um arquivo CSV. A ferramenta é útil para pesquisadores, analistas ou qualquer pessoa interessada em monitorar a cobertura da mídia sobre tópicos específicos ao longo do tempo.

## Funcionalidades

* **Busca por Palavras-Chave:** Permite a definição de consultas de busca complexas, combinando múltiplos termos com operadores lógicos `AND` e `OR`.
* **Filtragem por Período:** A busca é segmentada por ano, facilitando a coleta de dados históricos.
* **Controle de Limite:** É possível definir um limite máximo de notícias a serem coletadas por ano.
* **Exportação para CSV:** Os resultados são salvos em um arquivo CSV, contendo o título da notícia, o link e a data de publicação, organizados de forma cronológica.

## Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina (versão 3.6 ou superior).

As bibliotecas necessárias para a execução do script podem ser instaladas via `pip`. Crie um ambiente virtual (recomendado) e instale as dependências:

```bash
pip install pygooglenews
```
## Como Usar
**Clone o repositório:**
```bash
git clone https://github.com/viniciussilva010/News_Crawler
```
## Configuração da Busca:

Abra o arquivo busca2.py e configure os parâmetros de busca na seção if __name__ == '__main__':. 

**GRUPOS_TEMA**: Uma lista de listas que define a consulta lógica. Cada sublista é um grupo de termos conectados por AND, e os grupos são conectados por OR. 

  Exemplo:
  ```bash
    [["termoA", "termoB"], ["termoC", "termoD"]] se traduz em ("termoA" AND "termoB") OR ("termoC" AND "termoD").
```
**ANOS_PESQUISA**: Uma lista de anos para os quais a busca será realizada. 

**LIMITE_POR_ANO**: O número máximo de notícias a serem coletadas para cada ano. Defina como None para remover o limite. 

## Estrutura do Código
**montar_query_logica(lista_ou)**: Constrói a string de consulta lógica a partir da lista de grupos de busca.

**buscar_noticias(tema, ano, limite)**: Conecta-se à Google News para realizar a busca com base na consulta e no ano especificados.

**salvar_em_csv(noticias, nome_arquivo)**: Processa a lista de notícias, ordena-as por data de publicação e as salva em um arquivo CSV.

**if __name__ == '__main__':** : O bloco principal onde as configurações são definidas e a lógica de execução é orquestrada.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias ou correções.
