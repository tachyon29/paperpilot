import pymupdf

def extract_text_from_pdf(file_bytes: bytes):
    document = pymupdf.open(stream=file_bytes, filetype="pdf")

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    document.close()

    return pages

def chunk_pages(pages, chunk_size=1000, overlap=200):
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "page": page_number,
                    "text": chunk_text.strip()
                })

            start += chunk_size - overlap

    return chunks