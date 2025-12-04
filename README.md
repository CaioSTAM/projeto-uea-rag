# Assistente Virtual UEA — RAG + LLM Local

Este projeto implementa um **Assistente Virtual da UEA** baseado em **RAG (Retrieval-Augmented Generation)** utilizando:

- Extração e chunking de PDFs institucionais  
- Embeddings HuggingFace  
- Armazenamento vetorial com FAISS  
- Modelo LLM local (Qwen 0.5B Instruct)  
- API REST em FastAPI  
- Execução via Docker  

O objetivo é responder perguntas sobre documentos oficiais da UEA com base em um pipeline completo de recuperação + geração.

---------------------------------------------------------------------------------------------------------------

# Arquitetura Geral

A arquitetura segue o fluxo clássico de um sistema RAG:

PDFs -> Extração -> Chunking -> Embeddings

-> FAISS Index -> Recuperação semântica

-> LLM local (Qwen 0.5B) -> Respostas 

---------------------------------------------------------------------------------------------------------------

# **Componentes**

**ingest.py** - Carrega PDFs, divide em chunks, gera embeddings e salva o índice FAISS 
**FAISS** - Armazena vetores de embeddings (similaridade semântica) 
**HuggingFace Embeddings** - Modelo de embeddings (MiniLM-L6-v2) 
**LLM Local (Qwen 0.5B)** - Gera a resposta usando o contexto recuperado 
**rag.py** - Pipeline de recuperação e geração 
**FastAPI** - Camada HTTP expondo o endpoint `/ask` 
**Docker** - Empacota todo o sistema em um container executável 

---------------------------------------------------------------------------------------------------------------

# Como executar o projeto (Sem Docker)

## 1. Iniciar o Ambiente Virtual
```bash
python -m venv venv
venv\Scripts\activate
```
## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 3. Executar o pipeline de ingestão(Executar antes da API) 
```bash
python src/ingest.py
```

## 4. Iniciar a API

```bash
uvicorn api.main:app --reload
```
- fica disponível em: http://localhost:8000

---------------------------------------------------------------------------------------------------------------

# Como executar o projeto (Com Docker)

## 1. Executar o pipeline de ingestão
```bash
python src/ingest.py
```
- O ingest é executado fora do build afim de tornar a imagem leve.
## 2. Build da Imagem

```bash
docker build -t assistente-uea .
```

## 3. Rodar o conteiner 

```bash
docker run -p 8000:8000 assistente-uea
```

---------------------------------------------------------------------------------------------------------------

# Regenerar o indice

```bash
rm -r data/vectorstore
python src/ingest.py
```
---------------------------------------------------------------------------------------------------------------

# Chamando a API no terminal

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "O que é a UEA?"}'
```



