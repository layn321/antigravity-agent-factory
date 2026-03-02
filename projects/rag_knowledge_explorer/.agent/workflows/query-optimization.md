---
description: Optimization of search queries to improve RAG retrieval accuracy.
---

# Query Optimization Workflow

How to refine user queries for maximum retrieval effectiveness.

## Steps

1. **Query Expansion**
   - Generate 3-5 hypothetical answers (HyDE) or related keywords.
   - De-compose complex multi-part questions into sub-queries.

2. **Semantic Search**
   - Execute search with the expanded query set.
   - Apply MMR (Maximal Marginal Relevance) to ensure result diversity.

3. **Context Filtering**
   - Remove low-confidence or redundant chunks.
   - Sort chunks by semantic similarity and temporal relevance.

4. **Metadata Filtering**
   - Apply hard filters based on project tags or date ranges if specified.

5. **Final Ranking**
   - Present the top-K chunks to the generator.
