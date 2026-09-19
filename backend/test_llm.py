from llm import generate_answer


chunks = [
    {
        "page_number": 1,
        "content": "This paper proposes a new method for improving image classification accuracy."
    },
    {
        "page_number": 3,
        "content": "The proposed method achieved 94.2% accuracy on the ImageNet validation dataset."
    }
]

question = "What accuracy did the proposed method achieve?"

answer = generate_answer(question, chunks)

print("\nANSWER:\n")
print(answer)