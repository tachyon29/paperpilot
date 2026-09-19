from embedding import generate_embedding
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)

# Get one chunk that doesn't have an embedding yet
response = (
    supabase
    .table("document_chunks")
    .select("id, content")
    .is_("embedding", "null")
    .limit(1)
    .execute()
)

chunk = response.data[0]

print("Chunk ID:", chunk["id"])
print("Generating embedding...")

embedding = generate_embedding(chunk["content"])

print("Embedding dimensions:", len(embedding))

# Store the embedding
update_response = (
    supabase
    .table("document_chunks")
    .update({"embedding": embedding})
    .eq("id", chunk["id"])
    .execute()
)

print("Embedding stored successfully!")