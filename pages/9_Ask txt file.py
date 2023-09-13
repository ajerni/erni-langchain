import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
# from langchain.document_loaders import TextLoader
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from io import StringIO
import os
os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

st.header("Ask your txt file a question")

# Context
# loader= TextLoader("files/data.txt", encoding='utf-8')
# doc = loader.load()
# print(type(doc[0].page_content))

system_template="You answer all questions about this content: {content}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template="{question}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(llm=llm, prompt=chat_prompt)

uploaded_file = st.sidebar.file_uploader("Upload a txt file")

if not uploaded_file:
    st.info("Please upload txt file to continue.")
    st.stop()

stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

string_data = stringio.read() #mit streamlit eingelesen, also wird nicht auch noch der langchain TextLoader gebraucht!

# Enter your request here:
# my_question = "Wer hat im November Geburtstag?"
my_question = st.text_input("Gib Deine Frage an das Dokument ein:")

if my_question:
    
    response = chain.run(content=string_data, question=my_question)
    # response = chain.run(content=doc[0].page_content, question=my_question) //wenn langchain TextLoader genutzt würde

    st.write(response)
