from pdf_processor import extract_text_from_pdf, chunk_pages


with open("test.pdf", "rb") as f:
    file_bytes = f.read()

pages = extract_text_from_pdf(file_bytes)

chunks = chunk_pages(pages)

print("Pages:", len(pages))
print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- CHUNK {i + 1} | PAGE {chunk['page']} ---")
    print(chunk["text"])