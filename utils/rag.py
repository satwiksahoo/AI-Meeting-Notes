# import sys
# __import__("pysqlite3")
# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
# import os, glob
# from sentence_transformers import SentenceTransformer
# import chromadb
# from chromadb.config import Settings

# EMB_NAME = os.environ.get('EMB_MODEL', 'all-MiniLM-L6-v2')

# class RAGIndex:
#     # def __init__(self, persist_dir='rag_index'):
#     #     self.client = chromadb.Client(Settings(persist_directory=persist_dir, anonymized_telemetry=False))
#     #     # collection will be created if missing
#     #     self.collection = self.client.get_or_create_collection(name='knowledge_base')  ##
#     #     self.emb = SentenceTransformer(EMB_NAME)
        
#     def __init__(self, persist_dir='rag_index'):
#         # self.client = chromadb.Client(Settings(
#         #     chroma_db_impl="duckdb+parquet",
#         #     persist_directory=None,        # in-memory mode (no writes to read-only FS)
#         #     anonymized_telemetry=False
#         # ))
#         self.client = chromadb.Client(Settings(
#     chroma_db_impl="duckdb+parquet",
#     persist_directory="/mount/tmp/rag_index"
# ))
#         # collection will be created if missing
#         self.collection = self.client.get_or_create_collection(name='knowledge_base')
#         self.emb = SentenceTransformer(EMB_NAME)

#     def index_folder(self, folder='knowledge_base'): ##
#         docs, metadatas, ids = [], [], []
#         for i, path in enumerate(sorted(glob.glob(os.path.join(folder, '**', '*'), recursive=True))):
#             if os.path.isdir(path):
#                 continue
#             if not any(path.lower().endswith(ext) for ext in ['.md', '.txt']):
#                 continue
#             try:
#                 with open(path, 'r', encoding='utf-8', errors='ignore') as f:
#                     text = f.read().strip()
#                 if not text:
#                     continue
#                 docs.append(text)
#                 metadatas.append({'source': os.path.basename(path)})
#                 ids.append(f'doc_{i}')
#             except Exception:
#                 continue
#         if docs:
#             embs = self.emb.encode(docs).tolist()
#             self.collection.upsert(documents=docs, metadatas=metadatas, ids=ids, embeddings=embs)

#     def query(self, query_text, k=4):
#         if not query_text:
#             return []
#         q_emb = self.emb.encode([query_text]).tolist()
#         res = self.collection.query(query_embeddings=q_emb, n_results=k)
#         items = []
#         for doc, meta in zip(res.get('documents', [[]])[0], res.get('metadatas', [[]])[0]):
#             items.append({'text': doc, 'source': meta.get('source', 'knowledge_base')}) ##
#         return items



import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os, glob
from sentence_transformers import SentenceTransformer
import chromadb

EMB_NAME = os.environ.get('EMB_MODEL', 'all-MiniLM-L6-v2')

class RAGIndex:
    def __init__(self, persist_dir="/mount/tmp/rag_index"):
        # ✅ New API (Chroma >=0.5)
        self.client = chromadb.PersistentClient(path=persist_dir)
        # self.client.reset()    # newly added 

        # ✅ Collection auto-creates if missing
        self.collection = self.client.get_or_create_collection("knowledge_base")
        self.emb = SentenceTransformer(EMB_NAME)
        
    def index_folder(self, folder="knowledge_base", chunk_size=500):
        docs, metadatas, ids = [], [], []
        i = 0

        for path in sorted(glob.glob(os.path.join(folder, "**", "*"), recursive=True)):
            if os.path.isdir(path) or not any(path.lower().endswith(ext) for ext in [".md", ".txt"]):
                continue

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    while True:
                        text = f.read(5000)  # read in small batches instead of entire file
                        if not text:
                            break

                        for j in range(0, len(text), chunk_size):
                            chunk = text[j:j+chunk_size]
                            docs.append(chunk)
                            metadatas.append({"source": os.path.basename(path)})
                            ids.append(f"doc_{i}_{j}")
                i += 1
            except Exception:
                continue

            # flush every 1000 chunks to avoid memory spikes
            if len(docs) >= 1000:
                embs = self.emb.encode(docs).tolist()
                self.collection.upsert(documents=docs, metadatas=metadatas, ids=ids, embeddings=embs)
                docs, metadatas, ids = [], [], []

        # final flush
        if docs:
            embs = self.emb.encode(docs).tolist()
            self.collection.upsert(documents=docs, metadatas=metadatas, ids=ids, embeddings=embs)


    # def index_folder(self, folder="knowledge_base" ,chunk_size=500):
    #     docs, metadatas, ids = [], [], []
    #     for i, path in enumerate(sorted(glob.glob(os.path.join(folder, "**", "*"), recursive=True))):
    #         if os.path.isdir(path) or not any(path.lower().endswith(ext) for ext in [".md", ".txt"]):
    #             continue
    #         try:
    #             with open(path, "r", encoding="utf-8", errors="ignore") as f:
    #                 text = f.read().strip()
    #             if not text:
    #                 continue
                
    #             for j in range(0, len(text), chunk_size):
    #                 chunk = text[j:j+chunk_size]
    #                 docs.append(chunk)
    #                 metadatas.append({"source": os.path.basename(path)})
    #                 ids.append(f"doc_{i}_{j}")
    #             # docs.append(text)
    #             # metadatas.append({"source": os.path.basename(path)})
    #             # ids.append(f"doc_{i}")
    #         except Exception:
    #             continue

    #     if docs:
    #         embs = self.emb.encode(docs).tolist()
    #         self.collection.upsert(
    #             documents=docs, metadatas=metadatas, ids=ids, embeddings=embs
    #         )
    
    def query(self, query_text, k=4):
        if not query_text:
            return []
        q_emb = self.emb.encode([query_text]).tolist()
        res = self.collection.query(query_embeddings=q_emb, n_results=k)
        items = []
        for doc, meta in zip(res.get("documents", [[]])[0], res.get("metadatas", [[]])[0]):
            items.append({"text": doc, "source": meta.get("source", "knowledge_base")})
        return items
