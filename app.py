
import streamlit as st

from config import MAX_FILE_SIZE_MB
from document_processor import process_pdf
from rag_pipeline import ResearchPaperAssistant


st.set_page_config(
    page_title="Research Paper Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Research Paper Assistant")
st.write(
    "Upload a research paper, ask questions, and explore answers "
    "grounded in the document with page references."
)

with st.sidebar:
    st.header("About")
    st.write(
        "This application uses retrieval-augmented generation (RAG) "
        "to retrieve relevant passages before generating an answer."
    )
    st.caption("PDF text extraction only. Scanned PDFs require OCR.")

uploaded_file = st.file_uploader(
    "Upload a research paper (PDF)",
    type=["pdf"],
)

if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error(f"Please upload a PDF smaller than {MAX_FILE_SIZE_MB} MB.")
        st.stop()

    if st.session_state.get("uploaded_name") != uploaded_file.name:
        st.session_state.pop("assistant", None)
        st.session_state.pop("uploaded_name", None)

    if st.button("Process paper", type="primary"):
        try:
            with st.spinner("Extracting text and building the search index..."):
                chunks = process_pdf(uploaded_file.getvalue())
                assistant = ResearchPaperAssistant()
                chunk_count = assistant.index_chunks(chunks)

                st.session_state["assistant"] = assistant
                st.session_state["uploaded_name"] = uploaded_file.name

            st.success(
                f"Indexed {chunk_count} text chunks from {uploaded_file.name}."
            )
        except Exception as error:
            st.error(f"Could not process the paper: {error}")

assistant = st.session_state.get("assistant")

if assistant is not None:
    st.subheader("Ask your paper a question")

    question = st.text_input(
        "Your question",
        placeholder="What are the main findings of this paper?",
    )

    if st.button("Get answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Searching the paper and generating an answer..."):
                    result = assistant.answer_question(question)

                st.markdown("### Answer")
                st.write(result["answer"])

                st.markdown("### Retrieved source passages")
                for index, source in enumerate(result["sources"], start=1):
                    with st.expander(
                        f"Source {index} — Page {source['page_number']}"
                    ):
                        st.write(source["text"])
            except Exception as error:
                st.error(f"Unable to answer the question: {error}")
