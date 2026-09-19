import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def generate_answer(question: str, chunks: list):
    context_parts = []

    for chunk in chunks:
        context_parts.append(
            f"[Page {chunk['page_number']}]\n{chunk['content']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a research assistant.

Answer the user's question using ONLY the provided context.

If the context does not contain enough information to answer the question,
say that you could not find the answer in the document.

Always cite the page number when making a factual claim.

User question:
{question}

Context:
{context}
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt,
    )

    return response.text