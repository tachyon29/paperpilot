import os
from pydantic import BaseModel
from llm import generate_answer
from embedding import generate_embedding
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from supabase import create_client, Client
from pdf_processor import extract_text_from_pdf, chunk_pages
class QuestionRequest(BaseModel):
    question: str
    document_id: int
load_dotenv()

app = FastAPI()

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)


@app.get("/")
def home():
    return {"message": "PaperPilot backend is running"}


@app.get("/documents")
def get_documents():
    response = supabase.table("documents").select("*").execute()
    return response.data


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()

    storage_path = file.filename

    # 1. Upload PDF to Storage
    supabase.storage.from_("documents").upload(
        storage_path,
        file_bytes,
        {"content-type": "application/pdf"}
    )

    # 2. Save document metadata
    document = {
        "filename": file.filename,
        "storage_path": storage_path,
        "status": "processing"
    }

    response = supabase.table("documents").insert(document).execute()
    document_id = response.data[0]["id"]

    # 3. Extract text
    pages = extract_text_from_pdf(file_bytes)

    # 4. Create chunks
    chunks = chunk_pages(pages)

    # 5. Generate embeddings and prepare database rows
    chunk_rows = []

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk["text"])

        chunk_rows.append({
            "document_id": document_id,
            "page_number": chunk["page"],
            "chunk_index": index,
            "content": chunk["text"],
            "embedding": embedding
        })

    # 6. Insert all chunks
    if chunk_rows:
        supabase.table("document_chunks").insert(chunk_rows).execute()

    # 7. Mark document as processed
    supabase.table("documents").update({
        "status": "processed"
    }).eq("id", document_id).execute()

    return {
        "message": "PDF processed successfully",
        "document_id": document_id,
        "pages": len(pages),
        "chunks": len(chunks)
    }

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    # 1. Convert question into an embedding
    query_embedding = generate_embedding(request.question)

    # 2. Retrieve the most relevant chunks
    response = supabase.rpc(
    "match_document_chunks",
    {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter_document_id": request.document_id
    }
).execute()

    chunks = response.data

    # 3. Generate answer using retrieved chunks
    answer = generate_answer(
        request.question,
        chunks
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "page": chunk["page_number"],
                "similarity": chunk["similarity"]
            }
            for chunk in chunks
        ]
    }