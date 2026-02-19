"""
RAG-based knowledge base for debt collection domain knowledge.

Uses OpenAI embeddings + pgvector for vector storage via LangChain.
"""

import structlog
from pathlib import Path

logger = structlog.get_logger()

KNOWLEDGE_DIR = Path(__file__).parent.parent.parent.parent / "knowledge"


class KnowledgeBase:
    def __init__(self):
        self.retriever = None
        self.is_initialized = False

    async def initialize(self):
        """Load knowledge documents and create vector index with OpenAI embeddings."""
        try:
            from langchain_community.document_loaders import DirectoryLoader, TextLoader
            from langchain_community.vectorstores import PGVector
            from langchain_openai import OpenAIEmbeddings
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from app.config import get_settings

            settings = get_settings()

            embeddings = OpenAIEmbeddings(
                model=settings.openai_embedding_model,
                api_key=settings.openai_api_key,
            )

            loader = DirectoryLoader(
                str(KNOWLEDGE_DIR),
                glob="**/*.txt",
                loader_cls=TextLoader,
            )
            documents = loader.load()

            if not documents:
                logger.warning("knowledge_base_no_documents", path=str(KNOWLEDGE_DIR))
                self.is_initialized = True
                return

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)

            # Use sync PGVector (LangChain community doesn't have full async support)
            connection_string = settings.database_url.replace(
                "postgresql+asyncpg://", "postgresql+psycopg2://"
            )
            vectorstore = PGVector.from_documents(
                documents=chunks,
                embedding=embeddings,
                connection_string=connection_string,
                collection_name="knowledge_base",
                pre_delete_collection=False,
            )
            self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            self.is_initialized = True
            logger.info("knowledge_base_initialized", chunks=len(chunks))

        except Exception as e:
            logger.error("knowledge_base_init_error", error=str(e))
            self.is_initialized = True  # mark as done to avoid retry loops

    async def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        """
        Retrieve relevant knowledge passages for a given query.

        Args:
            query: The search query.
            top_k: Number of passages to retrieve.

        Returns:
            List of relevant text passages.
        """
        if not self.is_initialized:
            await self.initialize()

        if self.retriever is None:
            return []

        try:
            results = self.retriever.invoke(query)
            return [doc.page_content for doc in results[:top_k]]
        except Exception as e:
            logger.error("knowledge_retrieve_error", error=str(e))
            return []
