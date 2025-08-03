# LegalBotX

A Django project for uploading, processing, chunking, embedding, and searching SCN (PDF) files via REST API and Weaviate vector search.

## Features

- Upload SCN (PDF) files through a REST API endpoint
- Extracts text from PDFs (using PyPDF2 and OCR fallback)
- Chunks extracted text and generates embeddings
- Uploads chunks and embeddings to Weaviate
- Search and Q&A over uploaded content using OpenAI (Azure) and vector search

## Requirements

- Python 3.8+
- Django 5.2.4
- djangorestframework
- PyPDF2, pdf2image, pytesseract, sentence-transformers, weaviate-client, langchain-openai, python-dotenv

## Environment Variables

Set these in your `.env` file or environment:

| Variable             | Description                             |
| -------------------- | --------------------------------------- |
| `WEAVIATE_URL`     | Weaviate Cloud cluster URL              |
| `WEAVIATE_API_KEY` | Weaviate Cloud API key                  |
| `HF_API_KEY`       | HuggingFace API key for embedding model |
| `OPENAI_API_KEY`   | OpenAI API key for Azure OpenAI         |

## Important Notes

- **Weaviate Cloud is free for 15 days.** You must sign up for your own Weaviate Cloud cluster and use your own credentials (`WEAVIATE_URL`, `WEAVIATE_API_KEY`).
- **OpenAI API Key:** You must use your own OpenAI API key (`OPENAI_API_KEY`) for the Q&A functionality.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd legalbotx
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### 1. Upload SCN File

- **POST** `/api/upload/`
- **Body:** `file` (multipart/form-data, PDF file)
- **Functionality:**
  - Saves the uploaded file
  - Extracts text from the PDF (using PyPDF2, falls back to OCR if needed)
  - Chunks the text and generates embeddings
  - Uploads chunks and embeddings to Weaviate
  - Returns the file path and extracted text

### 2. Ask a Question

- **POST** `/api/ask/`
- **Body:** `query` (string)
- **Functionality:**
  - Searches for the most relevant chunks in Weaviate using vector search
  - Combines the top 3 chunks as context
  - Uses Azure OpenAI to generate an answer based on the context
  - Returns the answer

## Key Functions & Their Roles

- **extract_text_auto(pdf_path):** Extracts text from a PDF using PyPDF2, falls back to OCR if needed.
- **chunk_text(text, max_chunk_size=512):** Splits text into manageable chunks for embedding.
- **get_embeddings(chunks):** Generates embeddings for each chunk using SentenceTransformer.
- **upload_chunks(chunks, embeddings, source):** Uploads chunks and their embeddings to Weaviate.
- **search_legal_chunks(query, top_k=3):** Finds the most relevant chunks for a query using vector search.
- **generate_answer_from_context(query, context):** Uses Azure OpenAI to generate an answer from the context.
- **answer_query(query):** Orchestrates search and answer generation for a user query.

## Project Structure

- `scn/` - Django app for SCN file uploads, processing, and API endpoints
- `legalbotx/` - Project settings and configuration
