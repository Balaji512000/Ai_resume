# PRIA - Developer Guide & Dependency Map

Welcome to the Personal Resume AI Assistant (PRIA) codebase. If you want to modify this application, you need to know how the files connect. This guide tells you exactly **where to make a change** and **what else you need to update** when you do it.

## Quick File Dependency Map

1. **`app.py`** 
   - **What it does:** The frontend (Streamlit). Buttons, chat UI, file upload widgets.
   - **Depends on:** `backend/core/database.py` (to upload), `backend/core/agent.py` (to chat).

2. **`backend/config.py`**
   - **What it does:** Central settings (LLM model name, chunk size, prompt).
   - **Depends on:** Nothing. (Everything depends on *it*).

3. **`backend/core/database.py`**
   - **What it does:** Reads the file, splits text, creates FAISS embeddings.
   - **Depends on:** `backend/utils/parsers.py` (to read PDFs) and `backend/config.py` (for chunk sizes).

4. **`backend/core/agent.py`**
   - **What it does:** Takes the user question, searches FAISS, talks to Ollama LLM.
   - **Depends on:** `backend/core/database.py` (to load FAISS) and `backend/config.py` (for models/prompts).

5. **`backend/utils/parsers.py`**
   - **What it does:** Extracts text from PDFs and DOCXs.
   - **Depends on:** Nothing.

---

## "If I want to change X, where do I go?"

### 1. I want to change the LLM Model (e.g., from llama3.2:1b to mistral)
* **File to modify:** `backend/config.py`
* **What to do:** Change `LLM_MODEL = "llama3.2:1b"` to your new model name.
* **Other files to update:** None! Just make sure you ran `ollama pull <new_model>` in your terminal.

### 2. I want to change how the AI talks (e.g., make it nicer instead of strict)
* **File to modify:** `backend/config.py`
* **What to do:** Edit the text inside the `HR_SYSTEM_PROMPT` variable.
* **Other files to update:** None! `agent.py` automatically pulls this prompt.

### 3. I want to change the App Title, Colors, or Chat bubbles
* **File to modify:** `app.py`
* **What to do:** Change `st.title()`, `st.markdown()`, or edit the `st.chat_message()` loops.
* **Other files to update:** None! The backend doesn't care about the UI.

### 4. I want to add support for a new file type (e.g., `.txt` files)
* **File to modify #1:** `backend/utils/parsers.py`
  - *What to do:* Add a new function: `def extract_text_from_txt(file_path): ...`
* **File to modify #2:** `backend/core/database.py`
  - *What to do:* In `process_file_and_create_db()`, add an `elif ext == ".txt":` and call your new function.
* **File to modify #3:** `app.py`
  - *What to do:* Update the file uploader widget: `st.file_uploader(..., type=["pdf", "docx", "txt"])`

### 5. I want to change how much text the AI reads at once (Chunk Size)
* **File to modify:** `backend/config.py`
* **What to do:** Change `CHUNK_SIZE` or `CHUNK_OVERLAP`. 
* **Other files to update:** None in the code, BUT you must click **"Delete Current Resume"** and re-upload your resume so the database is rebuilt with the new sizes.

### 6. I want to add a new "Error Message" (e.g., File Too Big Error)
* **File to modify #1:** `backend/exceptions/custom_exceptions.py`
  - *What to do:* Add `class FileTooBigError(Exception): pass`
* **File to modify #2:** `backend/core/database.py`
  - *What to do:* Import your new error and `raise FileTooBigError("File is over 5MB")` when appropriate.
* **File to modify #3:** `app.py`
  - *What to do:* Add `FileTooBigError` to the `except (..., FileTooBigError):` block so the UI knows how to print it in red.
