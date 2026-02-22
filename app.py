import streamlit as st

st.set_page_config(page_title="App Moved", page_icon="🚫")

st.warning("🚨 **The application structure has been updated for better organization.** 🚨")
st.error("The main entry point has been moved to the `frontend/` directory.")

st.markdown("### How to run the app now:")
st.code("streamlit run frontend/app.py", language="bash")

st.info("Please update any of your scripts or shortcuts to use the new path.")
