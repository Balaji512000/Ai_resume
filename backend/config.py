"""Global settings and configurations for the application."""
import os
from dotenv import load_dotenv

# Load local .env if available
load_dotenv()

# LLM model configurations
FAISS_DB_PATH = "faiss_index"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = "llama-3.1-8b-instant" # Latest Groq lightning fast model
EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Free local lightweight model

# RAG tuning parameters
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
RETRIEVAL_K = 4
LLM_NUM_PREDICT = 120
LLM_TEMPERATURE = 0.0

# Base system prompt for the AI assistant 
HR_SYSTEM_PROMPT = """You are a helpful HR assistant.
Your job is to answer questions based strictly on the resume text provided below.

Resume Text Provided:
---------------------
{context}
---------------------

Instructions:
1. Answer the user's question directly, concisely, and in 1-2 short sentences maximum.
2. The candidate's name, email, and phone number are usually at the very beginning in "[Start of Resume]".
3. For skills, experience, and other queries, look into "[Relevant Matches]".
4. If the answer cannot be found in the text, reply exactly with: "This information is not mentioned in the resume."
5. Do not guess, assume, or use outside knowledge. Do not apologize."""
