import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.utilities import TextRequestsWrapper
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets["openai_api_key"])

requests_tools = load_tools(["requests_all"])

requests = TextRequestsWrapper()

text_data = requests.get("https://www.google.com/")

loader = TextLoader(text_data)
documents = loader.load()


# Get your splitter ready
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

# Split your docs into texts
texts = text_splitter.split_documents(documents)

# There is a lot of complexity hidden in this one line. I encourage you to check out the video above for more detail
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
result = chain.run(texts)

# template = """
# Give me five bullet points about the content of the following website:
# {req_data}
# """
#
# prompt = PromptTemplate(
#     input_variables=["req_data"],
#     template=template,
# )
#
#
# final_prompt = prompt.format(req_data=blick_data)
#
# result = llm(final_prompt)

st.write(result)


