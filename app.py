import streamlit as st
from rag import ask_question

st.set_page_config(page_title="Chat with your PDF", page_icon="📄")
st.title("📄 Chat with your PDF")

# Keep messages during Streamlit reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ask a new question
question = st.chat_input("Ask a question about the document")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the PDF..."):
            answer, pages = ask_question(question)

        st.markdown(answer)
        if pages:
            st.caption("Retrieved pages: " + ", ".join(map(str, pages)))

    # Save answer and page references for the next rerun
    saved_answer = answer
    if pages:
        saved_answer += "\n\n**Retrieved pages:** " + ", ".join(map(str, pages))

    st.session_state.messages.append(
        {"role": "assistant", "content": saved_answer}
    )