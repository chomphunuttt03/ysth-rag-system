# from src.ingest import get_embed_model, load_or_build_index
# from src.query import create_query_engine
# from src.app import get_llm
# from dotenv import load_dotenv

# load_dotenv()  

# def main():
#     embed_model = get_embed_model()
#     llm = get_llm()
#     index = load_or_build_index(embed_model)
#     engine = create_query_engine(index, llm)

#     print("\n✅ Thai Securities Q&A Ready! Type 'exit' to quit.\n")
#     while True:
#         query = input("❓ Question: ").strip()
#         if query.lower() in ["exit", "quit"]:
#             break
#         if not query:
#             continue
#         engine.ask(query)

# if __name__ == "__main__":
#     main()

import time
from src.ingest import get_embed_model, load_or_build_index
from src.query import create_query_engine
from src.app import get_llm
from dotenv import load_dotenv

load_dotenv()  

def main():
    embed_model = get_embed_model()
    llm = get_llm()
    index = load_or_build_index(embed_model)
    engine = create_query_engine(index, llm)

    print("\n✅ Thai Securities Q&A Ready! Type 'exit' to quit.\n")

    while True:
        query = input("❓ Question: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if not query:
            continue

        print(f"[DEBUG] query = {query}")

        start = time.time()
        result = engine.ask(query)
        end = time.time()

        print("\n🧠 Answer:\n")
        print(result)

        print(f"\n⏱ Response time: {end - start:.2f}s")
        print("-" * 50)

if __name__ == "__main__":
    main()