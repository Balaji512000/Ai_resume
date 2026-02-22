"""Main Streamlit UI application file."""
import streamlit as st
import sys
import os

# Add root project directory to Python path to import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# Import modular components
from backend.config import FAISS_DB_PATH, ADMIN_PASSWORD
from backend.core.database import VectorDBManager
from backend.core.agent import RAGPipeline
from backend.exceptions.custom_exceptions import UnsupportedFileFormatError, EmptyResumeError, VectorDatabaseError
from backend.utils.cache_manager import ResponseCache

# Enable sqlite caching (Langchain level)
set_llm_cache(SQLiteCache(database_path="llm_cache.db"))

FAQ_LIST = [
    "What is the candidate's full name?",
    "What is the candidate's email address?",
    "What is the candidate's phone number?",
    "Summarize the professional summary.",
    "What are the candidate's core skills?",
    "What is the candidate's total years of experience?",
    "What is the candidate's current or most recent job title?",
    "What are the candidate's educational qualifications?",
    "What major projects has the candidate worked on?",
    "Does the candidate have experience with Python?",
    "Does the candidate have experience with React?",
    "What certifications does the candidate hold?",
    "What languages can the candidate speak?",
    "What is the candidate's LinkedIn profile?",
    "Where is the candidate located?",
    "Does the candidate have leadership or management experience?",
    "Which databases is the candidate familiar with?",
    "What is the candidate's highest degree earned?",
    "What cloud platforms (AWS, Azure, GCP) does the candidate know?",
    "Can you list the candidate's soft skills?"
]

st.set_page_config(page_title="Personal Resume AI Assistant", page_icon="📄", layout="wide")

def main():
    st.title("📄 Personal Resume AI Assistant (vayu)")
    st.markdown("Your private, local AI assistant verified to answer queries directly from the uploaded resume using 100% Free architecture.")

    # Sidebar for File Uploads
    with st.sidebar:
        # Secret Admin Password
        st.subheader("Admin Access")
        admin_password = st.text_input("Enter Password to Manage:", type="password")
        admin_mode = (admin_password == ADMIN_PASSWORD)
        
        if admin_mode:
            st.header("Admin: Resume Management")
            uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX)", type=["pdf", "docx"])
            
            if uploaded_file:
                if st.button("Process & Upload Resume"):
                    with st.spinner("Processing text and generating embeddings..."):
                        try:
                            VectorDBManager.process_file_and_create_db(uploaded_file)
                            st.success("Resume successfully processed and indexed.")
                            st.session_state["messages"] = [] # Clear chat
                        except (UnsupportedFileFormatError, EmptyResumeError, VectorDatabaseError) as e:
                            st.error(str(e))
                        except Exception as e:
                            st.error(f"An unexpected error occurred: {str(e)}")
                            
            st.divider()
            if st.button("Delete Current Resume (Admin)"):
                VectorDBManager.delete_db()
                st.session_state["messages"] = []
                st.success("Current Resume (and memory) completely purged.")
        else:
            st.info("Upload functionality is disabled for viewers. Switch to Admin mode to manage resumes.")

        st.divider()
        st.subheader("Frequently Asked Questions (FAQ)")
        selected_test_q = st.selectbox("Select a query to ask the AI instantly:", FAQ_LIST)
        test_q_submitted = st.button("Ask FAQ ⚡")
        
        st.divider()
        st.subheader("System Status")
        if os.path.exists(FAISS_DB_PATH):
            st.success("🟢 Resume Indexed & AI Ready")
        else:
            st.error("🔴 No Resume Uploaded")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Render chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("source"):
                with st.expander("Show Evidence (Source Reference)"):
                    st.text(msg["source"])


    if os.path.exists(FAISS_DB_PATH):
        chat_q = st.chat_input("Ask a question about the uploaded resume...")
        user_query = chat_q if chat_q else (selected_test_q if test_q_submitted else None)
        
        if user_query:
            
            st.session_state["messages"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)


            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("*(Thinking...)* ⏳")
                
                try:
                    cached_response = ResponseCache.get(user_query)
                    
                    if cached_response:
                        full_response = cached_response
                        source_text = "Retrieved instantly from fast cache ⚡"
                        message_placeholder.markdown(full_response)
                    else:
                        streamer, docs = RAGPipeline.answer_query(user_query)
                        
                        if streamer is None:
                            full_response = docs
                            source_text = ""
                            message_placeholder.markdown(full_response)
                        else:
                            full_response = ""
                            for chunk in streamer:
                                full_response += chunk
                                message_placeholder.markdown(full_response + "▌")
                            
                            message_placeholder.markdown(full_response)
                            source_text = "\n\n---\n\n".join([f"Chunk:\n{doc.page_content}" for doc in docs])
                            if source_text:
                                with st.expander("Show Evidence (Source Reference)"):
                                    st.text(source_text)
                            
                        # Save successful answers to fast cache
                        if full_response and "Failed to connect" not in full_response:
                            ResponseCache.set(user_query, full_response.strip())
                            
                except Exception as e:
                    full_response = f"Failed to connect to backend AI/Ollama. Please ensure Ollama is running. Error: {str(e)}"
                    message_placeholder.markdown(full_response)
                    source_text = ""
                

                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": full_response.strip(),
                    "source": source_text
                })
    else:
        st.info("Please upload a resume on the sidebar to begin checking facts.")

if __name__ == "__main__":
    main()
