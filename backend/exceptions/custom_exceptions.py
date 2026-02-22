"""
Custom exception classes for cleaner error handling across the app.
"""
class DocumentProcessingError(Exception):
    """Failed to extract text from the file."""
    pass

class UnsupportedFileFormatError(Exception):
    """File isn't a PDF or DOCX."""
    pass

class EmptyResumeError(Exception):
    """Extracted text was empty (maybe an image-only PDF)."""
    pass

class VectorDatabaseError(Exception):
    """Something went wrong while building the FAISS index."""
    pass

class LLMConnectionError(Exception):
    """Couldn't connect to Ollama or the LLM."""
    pass
