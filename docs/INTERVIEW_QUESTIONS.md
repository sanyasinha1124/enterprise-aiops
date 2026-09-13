# Interview Questions

## LLM

### 1. What is an LLM?
A neural language model trained on large corpora to model token sequences and generate text.

### 2. Training vs inference?
Training updates model parameters using data and a loss function. Inference uses fixed parameters to generate predictions.

### 3. Why are tokens important?
Models operate on tokens rather than raw words. Token count affects context usage, latency and cost.

### 4. What is an embedding?
A dense vector representation designed to capture semantic information.

## RAG

### 5. Why use RAG instead of putting documents into model weights?
RAG keeps knowledge external, easier to update, inspect and restrict to relevant context.

### 6. RAG vs fine-tuning?
RAG changes the context supplied at inference. Fine-tuning changes model parameters.

### 7. What causes poor RAG?
Bad chunking, weak embeddings, wrong top-k, irrelevant retrieval, missing metadata filters, or poor generation prompts.

## Agents

### 8. What is function calling?
The model returns a structured request for an application-defined function. The application executes it and sends the result back to the model.

### 9. Can the LLM execute arbitrary Python?
Not in this design. Tools are allow-listed and executed by application code.

### 10. Why is tool security important?
An agent can cause real side effects. Tools need authentication, authorization, validation, least privilege and often human confirmation.

## Evaluation

### 11. What would you measure?
Retrieval quality, answer correctness/faithfulness/relevance, tool accuracy, latency, token usage and failure rates.

### 12. Why not report made-up accuracy?
Evaluation metrics are only meaningful when measured on a defined test set with a reproducible procedure.
