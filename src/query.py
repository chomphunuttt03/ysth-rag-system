class QueryEngine:
    def __init__(self, index, llm):
        self.retriever = index.as_retriever(similarity_top_k=8)
        self.llm = llm

    def ask(self, query: str):

        query_en = self.llm.complete(
            f"Translate to English (search query only):\n{query}"
        )

        nodes = self.retriever.retrieve(str(query_en))

        if not nodes:
            return {
                "answer": "Not found in data",
                "sources": []
            }

        context = "\n\n".join([n.node.get_content() for n in nodes])

        prompt = f"""
You are a financial analyst.

Context:
{context}

Question:
{query}

Answer:
"""
        answer = self.llm.complete(prompt)

        sources = []
        for n in nodes:
            sources.append(n.node.metadata.get("file_name", "unknown"))

        return {
            "answer": str(answer),
            "sources": list(set(sources))
        }

def create_query_engine(index, llm):
    return QueryEngine(index, llm)
