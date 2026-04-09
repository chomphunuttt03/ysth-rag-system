import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

PERSIST_DIR = "./storage"
DATA_DIR = "./data"


def get_embed_model():
    return HuggingFaceEmbedding(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        normalize=True
    )


def build_index(embed_model):
    print("🔄 Loading documents...")
    documents = SimpleDirectoryReader(DATA_DIR, recursive=True).load_data()
    print(f"✅ Loaded {len(documents)} documents")

    splitter = SentenceSplitter(chunk_size=256, chunk_overlap=80)

    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model,
        transformations=[splitter],
        show_progress=True
    )

    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("✅ Index saved")

    return index


def load_or_build_index(embed_model):
    Settings.embed_model = embed_model  

    if os.path.exists(PERSIST_DIR):
        print("✅ Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context)

    return build_index(embed_model)
