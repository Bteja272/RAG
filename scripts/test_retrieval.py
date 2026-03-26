from app.services.retrieval_service import RetrievalService


def main():
    query = "How does retrieval-augmented generation improve response grounding?"
    results = RetrievalService.retrieve(query=query, top_k=3)

    print(f"Retrieved {len(results)} chunks:\n")

    for index, result in enumerate(results, start=1):
        print(f"Result {index}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Document ID: {result['document_id']}")
        print(f"Chunk Index: {result['chunk_index']}")
        print(f"Page Number: {result['page_number']}")
        print(f"Text: {result['text']}\n")


if __name__ == "__main__":
    main()