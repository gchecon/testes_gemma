# testes_gemma
Testes da viabilidade de uso do LLM Gemma

O Documento Base do teste está em 

> [Medium] https://medium.com/towards-artificial-intelligence/building-rag-application-using-gemma-7b-llm-upstash-vector-database-ff50b715d906

# Construindo Aplicação RAG com Gemma 7B LLM & Upstash Vector Database

Por Youssef Hosni, publicado em Towards AI, 8 de Março de 2024.

## Resumo

Este artigo oferece um guia passo a passo para construir uma aplicação completa de Geração Aumentada por Recuperação (RAG) utilizando o último modelo de linguagem de grande porte (LLM) de código aberto do Google, Gemma 7B, e o banco de dados vetorial serverless da Upstash. O conceito RAG envolve fornecer LLMs com informações adicionais de uma fonte de conhecimento externa, permitindo gerar respostas mais precisas e contextualizadas enquanto reduz alucinações.

## Índice

1. Introdução e Configuração do Ambiente de Trabalho
2. Download e Divisão do Dataset Cosmopedia
3. Geração de Embeddings com o Modelo de Transformadores de Sentença
4. Armazenamento dos Embeddings no Banco de Dados Vetorial da Upstash
5. Introdução e Uso do Gemma 7B LLM
6. Consultando a Aplicação RAG

## 1. Introdução e Configuração do Ambiente de Trabalho

- Preparação do ambiente inclui a instalação de pacotes necessários e importação de bibliotecas.
- Conceitos fundamentais do RAG: Componentes de recuperação e geração.

## 2. Download e Divisão do Dataset Cosmopedia

- Seleção do subset 'Stanford' do Cosmopedia, um dos maiores datasets sintéticos abertos disponíveis.
- Processo de conversão para Pandas dataframe e subsequente divisão em pedaços menores para adequação ao contexto do modelo.

## 3. Geração de Embeddings com o Modelo de Transformadores de Sentença

- Uso do modelo all-MiniLM-L6-v2 para geração de embeddings.
- Importância dos embeddings na melhoria da precisão de recuperação.

## 4. Armazenamento dos Embeddings no Banco de Dados Vetorial da Upstash

- Configuração e uso do Upstash Vector, um banco de dados vetorial serverless.
- Armazenamento de embeddings gerados para posterior recuperação e uso.

## 5. Introdução e Uso do Gemma 7B LLM

- Detalhes sobre a família de modelos LLM Gemma do Google.
- Processo de inicialização e uso do modelo para geração de texto.

## 6. Consultando a Aplicação RAG

- Método para consulta e geração de respostas baseadas em embeddings e LLM.
- Exemplo de uso com a pergunta "Escreva uma história educativa para crianças pequenas."

Este artigo serve como um guia detalhado para construir e consultar uma aplicação RAG, demonstrando a potencialidade dos LLMs quando combinados com tecnologias de banco de dados vetoriais.
