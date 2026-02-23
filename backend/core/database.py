"""Manages the FAISS vector database initialization and operations."""
import os
import shutil
import tempfile
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import FAISS_DB_PATH, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, PROJECT_ROOT
from backend.utils.parsers import extract_text_from_pdf, extract_text_from_docx
from backend.exceptions.custom_exceptions import UnsupportedFileFormatError, EmptyResumeError, VectorDatabaseError
from backend.utils.cache_manager import ResponseCache

RESUME_START_FILE = os.path.join(PROJECT_ROOT, "resume_start.txt")

class VectorDBManager:
    """Wrapper class for FAISS operations."""
    
    @staticmethod
    def process_file_and_create_db(uploaded_file):
        """Takes an uploaded file, extracts text, and builds the FAISS index."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext == ".pdf":
                text = extract_text_from_pdf(tmp_path)
            elif ext == ".docx":
                text = extract_text_from_docx(tmp_path)
            else:
                raise UnsupportedFileFormatError("Please strictly upload a PDF or DOCX resume.")

            if not text.strip():
                raise EmptyResumeError("Empty resume or unreadable scanned image. File must contain real text.")

            # Clear old index to maintain single resume state
            VectorDBManager.delete_db()

            # Save the first 1000 characters to ensure Name/Contact info is never missed by vector search
            with open(RESUME_START_FILE, "w", encoding="utf-8") as f:
                f.write(text[:1000])

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            chunks = text_splitter.split_text(text)

            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            vector_db = FAISS.from_texts(chunks, embeddings)
            vector_db.save_local(FAISS_DB_PATH)

            return True

        except (UnsupportedFileFormatError, EmptyResumeError) as e:
            raise e
        except Exception as e:
            raise VectorDatabaseError(f"Vector Indexing Failed: {str(e)}")
        finally:
            os.remove(tmp_path)

    @staticmethod
    def delete_db():
        """Wipes the FAISS index directory and clears cache."""
        if os.path.exists(FAISS_DB_PATH):
            shutil.rmtree(FAISS_DB_PATH)
        if os.path.exists(RESUME_START_FILE):
            os.remove(RESUME_START_FILE)
        ResponseCache.clear()

    @staticmethod
    def load_db():
        """Loads the active FAISS index."""
        if os.path.exists(FAISS_DB_PATH):
            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            return FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        return None
