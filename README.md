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

**FastAPI** - Camada HTTP expondo os endpoints `/ask`, `/retrieve`, `/health` e `/stats`
 
**Docker** - Empacota todo o sistema em um container executável 

---------------------------------------------------------------------------------------------------------------

# Como executar o projeto com Docker

## 1. Build da Imagem

```bash
docker build -t assistente-uea .
```

## 3. Rodar o conteiner 

```bash
docker run -p 8000:8000 ^
  -v "%cd%/data/pdfs:/app/data/pdfs" ^
  assistente-uea
```

## 4. Acessar a documentação da API no navegador (localmente)

```bash
http://localhost:8000/docs
```

---------------------------------------------------------------------------------------------------------------

# Regenerar o indice

```bash
rmdir /s /q data\vectorstore
docker run -p 8000:8000 ^
  -v "%cd%/data/pdfs:/app/data/pdfs" ^
  assistente-uea
```
---------------------------------------------------------------------------------------------------------------

# Chamando a API no terminal

## /ASK

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Quais são os requisitos que o aluno deve atender para concorrer a uma vaga nas Casas do Estudantes da UEA?"}'
```

## /RETRIEVE

```bash
curl -X POST "http://localhost:8000/retrieve" \
     -H "Content-Type: application/json" \
     -d '{"question": "requisitos para vaga na Casa do Estudante"}'
```

## /HEALTH

```bash
curl http://localhost:8000/health
```

## /STATS

```bash
curl http://localhost:8000/stats
```





