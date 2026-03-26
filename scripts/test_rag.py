from app.services.rag_service import RAGService


def main():
    query = "What is Retrieval-Augmented Generation?"

    response = RAGService.query(query)

    print("\n=== QUERY ===")
    print(response["query"])

    print("\n=== ANSWER ===")
    print(response["answer"])

    print("\n=== SOURCES ===")
    for i, src in enumerate(response["sources"], 1):
        print(f"\nSource {i}:")
        print(src["text"])


if __name__ == "__main__":
    main()