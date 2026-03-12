# AI-Powered Product Knowledge Search (RAG) — Chemical/Pharma Industry

A simple RAG-based search engine over dummy chemical/pharma CSV data.

**Tech Stack:**
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB:** Pinecone (serverless)
- **LLM:** Ollama `mistral:7b-instruct-q4_K_M` (runs locally)
- **API:** FastAPI
- **Exports:** Excel, PDF, PowerPoint, PNG bar chart

---

## Project Structure

```
Pharma ragchatbot/
├── data/                  # 14 dummy CSV files
├── app.py                 # FastAPI application
├── build_index.py         # Embeds data → Pinecone
├── data_loader.py         # Loads + unifies all CSVs
├── config.py              # Central configuration
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your Pinecone API key
```

### 3. Start Ollama (if not running)

```bash
ollama pull mistral:7b-instruct-q4_K_M
ollama serve
```

### 4. Build the vector index

```bash
python build_index.py
```

### 5. Start the API server

```bash
python app.py
# or: uvicorn app:app --reload --port 8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/search?query=<text>` | Search + AI summary |
| `GET` | `/export/excel?query=<text>` | Download `.xlsx` |
| `GET` | `/export/pdf?query=<text>` | Download `.pdf` |
| `GET` | `/export/ppt?query=<text>` | Download `.pptx` |
| `GET` | `/export/graph?query=<text>` | Download `.png` chart |

### Example Queries

```
/search?query=Find suppliers of Metformin in Europe
/search?query=API manufacturers certified with ISO in India
/search?query=Registered products in Argentina
```

---

## Interactive Docs

Visit **http://localhost:8000/docs** for the auto-generated Swagger UI.

screen shots of rag indexes and outputs:
<img width="1270" height="872" alt="image" src="https://github.com/user-attachments/assets/38bd0c1d-c5ae-4209-87cb-c9f3a1ce2cf7" />
<img width="1867" height="951" alt="image" src="https://github.com/user-attachments/assets/6612b55e-0449-43c2-bcea-f3734e78fb3c" />

<img width="1895" height="947" alt="image" src="https://github.com/user-attachments/assets/c73fa7e2-247d-465c-88f0-732b6c4d36ea" />

<img width="1867" height="989" alt="image" src="https://github.com/user-attachments/assets/fd10d720-43d2-41fe-9bc4-30e0f133e365" />




