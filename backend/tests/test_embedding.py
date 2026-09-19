from embedding import generate_embedding


text = "The proposed model achieved an accuracy of 94.2%."

embedding = generate_embedding(text)

print("Dimensions:", len(embedding))
print("First 10 values:", embedding[:10])