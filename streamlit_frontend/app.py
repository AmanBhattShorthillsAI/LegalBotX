import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("📄 LegalBotX - Your Legal Assistant")

# File upload
st.subheader("1. Upload a Legal PDF")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
if uploaded_file:
    with st.spinner("Uploading and extracting..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/api/upload/", files=files)
        print(f"true/false: {response.ok}")
        print(f"response: {response.json()}")
        if response.ok:
            st.success("✅ PDF processed successfully!")
            st.json(response.json())
        else:
            st.error("❌ Upload failed.")

# Ask a question
st.subheader("2. Ask a Legal Question")
question = st.text_input("Type your question here...")
if st.button("Ask"):
    if not question:
        st.warning("❗ Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            res = requests.post(f"{BACKEND_URL}/api/ask/", json={"query": question})
            if res.ok:
                answer = res.json().get("answer", "No answer returned.")
                st.markdown(f"**Answer:** {answer}")
            else:
                st.error("⚠️ Error during query.")
