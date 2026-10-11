# 📚 AI Research Paper Assistant — RAG

## Overview

The AI Research Paper Assistant is a document question-answering project built around Retrieval-Augmented Generation (RAG). It is designed to help users explore research papers by uploading a PDF and asking questions about its contents.

Instead of relying only on a language model's existing knowledge, the application retrieves relevant passages from the uploaded paper and uses those passages as context for generating an answer. Retrieved passages are displayed with page references to make it easier to check the source.

## Features

- PDF text extraction and document chunking.
- Semantic search using sentence embeddings.
- Vector storage and retrieval with ChromaDB.
- Context-grounded question answering through an OpenAI-compatible chat model.
- Page references and expandable source passages.
- Streamlit-based user interface.
- Unit tests for document processing and retrieval safeguards.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| User interface | Streamlit |
| PDF processing | pypdf |
| Embeddings | Sentence Transformers |
| Vector database | ChromaDB |
| Answer generation | OpenAI API |
| Configuration | python-dotenv |
| Testing | Pytest |

## Architecture

1. **Upload:** The user provides a research paper in PDF format.
2. **Extract:** Text is extracted from each PDF page.
3. **Chunk:** The text is divided into smaller, overlapping passages.
4. **Embed:** An embedding model converts passages into numerical vectors.
5. **Retrieve:** ChromaDB returns passages relevant to the user's question.
6. **Generate:** The language model receives the question and retrieved passages as context.
7. **Present:** The answer and supporting passages are displayed in the interface.

## Project Structure

```text
ai-research-paper-assistant/
├── app.py
├── rag_pipeline.py
├── document_processor.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    ├── test_document_processor.py
    └── test_rag_pipeline.py
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-research-paper-assistant.git
cd ai-research-paper-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a local `.env` file using `.env.example` as a template.

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Use your own valid API key and keep the `.env` file private. API usage may incur charges.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit in your browser.

## Running Tests

```bash
pytest -v
```

The tests cover document chunking, empty-document handling, and retrieval input safeguards. They do not by themselves validate answer quality or the complete RAG workflow.

## Current Limitations

- Text-based PDFs are supported; OCR for scanned documents is not included.
- The ChromaDB index is held in memory and is not persistent.
- Answers depend on the retrieved passages and the configured language model.
- API access and end-to-end behavior must be tested in a configured Python environment.

## Future Improvements

- Add OCR for scanned research papers.
- Evaluate retrieval quality and answer faithfulness using a defined test set.
- Add persistent storage and document-library management.
- Support multiple papers and conversation history.
- Add authentication, deployment, and usage monitoring.

## Learning Goals

This project explores document processing, embeddings, vector search, prompt design, and the fundamentals of building a RAG-based application.

