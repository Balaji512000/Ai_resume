import time
import sys
import os

# Add the parent directory to the Python path so we can import 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.agent import RAGPipeline
from backend.core.database import VectorDBManager
from backend.config import FAISS_DB_PATH

def run_performance_test(question: str):
    """Measures the latency of the RAG pipeline for a given question."""
    
    print(f"\n[{'-'*40}]")
    print(f"Test Query: '{question}'")
    print(f"[{'-'*40}]")

    # 1. Validation Check
    if not os.path.exists(FAISS_DB_PATH):
        print("❌ Error: No FAISS database found. Please upload a resume via the Streamlit app first.")
        return

    # 2. Total Execution Time Start
    start_time_total = time.time()

    try:
        # Request stream generator from backend
        pipeline_start = time.time()
        streamer, docs = RAGPipeline.answer_query(question)
        pipeline_end = time.time()
        
        if streamer is None:
            # Error / Fallback message
            print(f"Fallback/Error Response: {docs}")
            return
            
        print(f"✅ RAG Initialization & Document Retrieval Time: {(pipeline_end - pipeline_start):.3f} seconds")
        print(f"✅ Context Retrieved: {len(docs)} chunks.\n")
        
        print("Streaming Answer:")
        
        # 3. LLM Token Generation Time Start
        first_token_time = None
        chars_generated = 0
        
        for chunk in streamer:
            if first_token_time is None:
                first_token_time = time.time()
            chars_generated += len(chunk)
            print(chunk, end="", flush=True)

        print("\n")
        
        end_time_total = time.time()
        
        # 4. Final Metrics Calculation
        if first_token_time:
            time_to_first_token = first_token_time - pipeline_end
            gen_time = end_time_total - first_token_time
            print(f"[{' METRICS ':=^30}]")
            print(f"⏱️ Time to First Token (TTFT): {time_to_first_token:.3f} s")
            print(f"⏱️ Generation Time (Streaming): {gen_time:.3f} s")
            print(f"⏱️ Total Response Latency     : {(end_time_total - start_time_total):.3f} s")
            print(f"📊 Approximate Length         : {chars_generated} characters")
            print(f"[{'='*32}]\n")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")

if __name__ == "__main__":
    print("🚀 Starting PRIA Metrics & Latency Tester 🚀\n")
    
    # Standard questions to benchmark 1B model retrieval and speed
    test_questions = [
        "What is the candidate's name?",
        "How many years of experience does the candidate have?",
        "What are the main programming languages known?"
    ]

    for q in test_questions:
        run_performance_test(q)
        time.sleep(1) # Small pause between questions
