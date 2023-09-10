import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]

st.header("PDF Q+A Bot")

pdf = st.sidebar.file_uploader("load PDF file", type="pdf")

if not pdf:
    st.info("Please upload PDF file to continue.")
    st.stop()

if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(chunks, embeddings)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    def get_answer(question):
        similars = vectorstore.similarity_search(query=question, k=3)
        qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
        response = qa_chain.run(input_documents=similars, question=question)
        return response


    question = st.text_input("Question")

    if question:
        answer = get_answer(question)
        st.write(answer)
