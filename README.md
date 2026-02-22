<<<<<<< HEAD
# Ai_resume
AI Resume Assistant is a private, 100% free tool that helps HR professionals quickly understand a candidate from their resume. Built with Groq and LangChain, it analyzes an uploaded CV and turns it into an interactive Q&amp;A experience. Recruiters can ask about skills, experience, projects, and role suitability and receive instant, clear answers.
=======
# Personal Resume AI Assistant (PRIA)

This is a private, single-user system designed to act strictly as a verifier of resumes, answering your questions purely using extracted text without guessing or hallucinating.

## Requirements Checklist
1. **Python 3.8+**
2. **Ollama**:
   Since the PRD strictly forbids paid APIs, you **must use Ollama** to run LLMs and Embeddings locally.
   - Install Ollama from [https://ollama.com/](https://ollama.com/)
   - Open a new terminal and run:
     ```bash
     ollama pull llama3
     ollama pull nomic-embed-text
     ```
     *(This ensures the models are downloaded locally onto your computer)*

## Running the Application
Once dependencies are installed via `pip install -r requirements.txt` and the Ollama models are pulled:
1. Open a terminal in this directory.
2. Ensure Ollama is running in the background.
3. Start the UI:
   ```bash
   streamlit run frontend/app.py
   ```
4. A browser window will pop up at `http://localhost:8501`.

## Features
- **Upload Resume**: Supports PDF and DOCX. Automatically extracts and chunks text, then vectorizes it in a local FAISS DB.
- **Delete Resume**: Wipes the AI's memory and vectors related to the resume permanently.
- **Single Active Resume**: Uploading a new resume always deletes the previous one completely.
- **Strict Grounding**: The local Llama model has been strictly prompted to verify information and *refuse* to guess using the exact phrase: *"This information is not mentioned in the resume."*
- **Evidence Sources**: Every AI answer also displays a dropdown showing the exact raw text snippet used to produce the answer.
>>>>>>> f23e67f (Initial commit for Vayu Resume AI)
