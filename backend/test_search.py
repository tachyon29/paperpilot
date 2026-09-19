from embedding import generate_embedding
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)

question = "What is the main contribution of this paper?"

# Convert question into a vector
query_embedding = generate_embedding(question)

# Search for similar chunks
response = supabase.rpc(
    "match_document_chunks",
    {
        "query_embedding": query_embedding,
        "match_count": 5
    }
).execute()

for result in response.data:
    print("\n---")
    print("Page:", result["page_number"])
    print("Similarity:", result["similarity"])
    print("Content:", result["content"][:500])