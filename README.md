# PaperPilot

A document question-answering application built using Retrieval-Augmented Generation (RAG).

PaperPilot allows users to upload PDF documents and ask questions about their contents. The system retrieves the most relevant sections of the document and provides them as context to a Gemini language model to generate an answer with page-level sources.

## Overview

PaperPilot implements an end-to-end RAG pipeline:

1. A user uploads a PDF.
2. Text is extracted from each page using PyMuPDF.
3. The extracted text is split into overlapping chunks.
4. Each chunk is converted into a vector embedding using Gemini.
5. Embeddings and document metadata are stored in Supabase.
6. A user question is converted into an embedding.
7. Supabase performs vector similarity search to retrieve the most relevant chunks.
8. The retrieved chunks are passed to Gemini Flash as context.
9. The generated answer is returned along with the source page numbers.

## Architecture

```text
                    ┌─────────────────┐
                    │   React + Vite  │
                    │    Frontend     │
                    └────────┬────────┘
                             │
                             │ HTTP
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │     Backend     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      ┌────────────────┐           ┌────────────────┐
      │   PDF Upload   │           │ User Question  │
      └───────┬────────┘           └───────┬────────┘
              │                            │
              ▼                            ▼
      ┌────────────────┐           ┌────────────────┐
      │    PyMuPDF     │           │ Query Embedding│
      │ Text Extraction│           │     Gemini     │
      └───────┬────────┘           └───────┬────────┘
              │                            │
              ▼                            ▼
      ┌────────────────┐           ┌────────────────┐
      │ Chunking       │           │ Vector Search  │
      │ 1000 / 200     │           │    Supabase    │
      └───────┬────────┘           └───────┬────────┘
              │                            │
              ▼                            ▼
      ┌────────────────┐           ┌────────────────┐
      │ Gemini         │           │ Top 5 Relevant │
      │ Embeddings     │           │     Chunks     │
      └───────┬────────┘           └───────┬────────┘
              │                            │
              ▼                            ▼
      ┌────────────────────────────────────────────┐
      │              Supabase / pgvector           │
      └──────────────────────┬─────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Gemini Flash   │
                    │ Answer Generation│
                    └────────┬────────┘
                             │
                             ▼
                    Answer + Page Sources


## Limitations

- PDF processing currently focuses on text-based PDFs.
- Chunking is character-based rather than semantic.
- Retrieval currently uses a fixed top-5 result count.
- The system does not currently include a dedicated reranking stage.
- Document processing is performed during the upload request rather than through a background job.

## Future Improvements

- Add asynchronous document processing using a background job queue.
- Introduce semantic or structure-aware chunking.
- Add reranking to improve retrieval quality.
- Add evaluation metrics for retrieval and answer quality.
- Support additional document formats.
- Add authentication and multi-user document isolation.
- Improve observability with structured logging and metrics.