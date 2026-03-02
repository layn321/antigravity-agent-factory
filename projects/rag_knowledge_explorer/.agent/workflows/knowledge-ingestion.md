---
description: Pipeline for ingesting and indexing new knowledge into the RAG system.
---

# Knowledge Ingestion Workflow

This workflow ensures that new documents are processed correctly before being added to the vector store.

## Steps

1. **Pre-processing**
   - Clean the text (remove boilerplate, normalize whitespace).
   - Detect document structure (headers, metadata).

2. **Chunking Strategies**
   - Use semantic chunking based on header hierarchy.
   - Fallback to fixed-size chunks with 10% overlap if structure is unclear.

3. **Embedding**
   - Generate embeddings using specified model (default: `text-embedding-3-small`).
   - Batch process to optimize API costs.

4. **Indexing**
   - Upsert into the vector database.
   - Update `knowledge_metadata.json` with timestamp and source ID.

5. **Verification**
   - Perform a sample query to verify retrieval works for the new content.
