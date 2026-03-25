from app.services.embedding_service import EmbeddingService


def main():
    sample_text = "Retrieval-augmented generation improves grounded question answering."

    embedding = EmbeddingService.embed_text(sample_text)

    print(f"Embedding length: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}")


if __name__ == "__main__":
    main()