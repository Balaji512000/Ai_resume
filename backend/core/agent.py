"""RAG Pipeline module for querying the vector database."""
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.config import LLM_MODEL, RETRIEVAL_K, HR_SYSTEM_PROMPT, LLM_TEMPERATURE, GROQ_API_KEY, PROJECT_ROOT
from backend.core.database import VectorDBManager

RESUME_START_FILE = os.path.join(PROJECT_ROOT, "resume_start.txt")

class RAGPipeline:
    """Main RAG logic wrapper."""

    @staticmethod
    def answer_query(user_query: str):
        """Queries the LLM and returns a text stream + the retrieved documents."""
        vector_db = VectorDBManager.load_db()
        if not vector_db:
            return None, "Error: No resume index found."


        retriever = vector_db.as_retriever(search_kwargs={"k": RETRIEVAL_K})
        docs = retriever.invoke(user_query)
        context_texts = "\n\n".join([doc.page_content for doc in docs])

        try:
            with open(RESUME_START_FILE, "r", encoding="utf-8") as f:
                start_text = f.read()
            context_texts = f"[Start of Resume]\n{start_text}\n[End of Start]\n\n[Relevant Matches]\n{context_texts}"
        except Exception:
            pass

        if not docs or not context_texts.strip():
            return None, "This information is not mentioned in the resume."

        llm = ChatGroq(model_name=LLM_MODEL, temperature=LLM_TEMPERATURE, groq_api_key=GROQ_API_KEY)

        prompt = ChatPromptTemplate.from_messages([
            ("system", HR_SYSTEM_PROMPT),
            ("human", "{question}")
        ])

        chain = prompt | llm | StrOutputParser()
        

        return chain.stream({"context": context_texts, "question": user_query}), docs
