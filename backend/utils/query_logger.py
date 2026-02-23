"""
Query Logger — Works on Streamlit Cloud using Supabase (free) OR fallback to print logs.
Supabase free tier: 500MB storage, unlimited rows — enough for thousands of queries!
"""
import os
from datetime import datetime

# Try to import supabase — if not installed, fallback to print logging
try:
    from supabase import create_client
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False


def _get_supabase_client():
    """Returns a Supabase client using env vars."""
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    if url and key and SUPABASE_ENABLED:
        return create_client(url, key)
    return None


class QueryLogger:
    """
    Logs every user question with timestamp.
    - If Supabase env vars are set → saves to cloud DB (permanent!)
    - Otherwise → prints to console (visible in Streamlit Cloud Logs tab)
    """

    @staticmethod
    def log(query: str, answer: str, source: str = "live"):
        """Saves a question + answer + timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Always print to console (visible in Streamlit Cloud → Logs tab)
        print(f"[QUERY LOG] [{timestamp}] SOURCE={source} | Q: {query} | A: {answer[:100]}")

        # If Supabase configured → save to DB (permanent)
        client = _get_supabase_client()
        if client:
            try:
                client.table("query_logs").insert({
                    "timestamp": timestamp,
                    "question": query.strip(),
                    "answer": answer.strip()[:500],
                    "source": source
                }).execute()
            except Exception as e:
                print(f"[QUERY LOG] Supabase error: {e}")

    @staticmethod
    def get_all():
        """Returns all logged queries from Supabase (or empty list if not configured)."""
        client = _get_supabase_client()
        if client:
            try:
                result = client.table("query_logs").select("*").order("timestamp", desc=True).limit(100).execute()
                return result.data
            except Exception as e:
                print(f"[QUERY LOG] Supabase fetch error: {e}")
                return []
        return []  # No Supabase → no persistent logs

    @staticmethod
    def clear():
        """Clears all logs (admin only) — only works if Supabase is configured."""
        client = _get_supabase_client()
        if client:
            try:
                client.table("query_logs").delete().neq("id", 0).execute()
            except Exception as e:
                print(f"[QUERY LOG] Supabase clear error: {e}")
