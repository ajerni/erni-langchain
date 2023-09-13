import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.utilities import TextRequestsWrapper
#from langchain.chains.summarize import load_summarize_chain
#from langchain.document_loaders import TextLoader
#from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets["openai_api_key"])

requests_tools = load_tools(["requests_all"])

requests = TextRequestsWrapper()

text_data = requests.get("https://jsonplaceholder.typicode.com/todos/1")

#loader = TextLoader(text_data)
#documents = loader.load()


# Get your splitter ready
#text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=10)

# Split your docs into texts
#texts = text_splitter.split_documents(documents)

# There is a lot of complexity hidden in this one line. I encourage you to check out the video above for more detail
#chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
#result = chain.run(texts[:5])

template = """
Give me the title from the following document:
{req_data}
"""

prompt = PromptTemplate(
    input_variables=["req_data"],
    template=template,
)

final_prompt = prompt.format(req_data=text_data)

result = llm(final_prompt)

st.header("Request example")

st.markdown("[https://jsonplaceholder.typicode.com/todos/1](https://jsonplaceholder.typicode.com/todos/1)")

st.write(result)

# dweet.io Beispiel wie auf status.andierni.ch
import dweepy
st.write("Dweet.io Example")
my_text = "...waiting..."
st.write("Test it like: 'https://dweet.io/dweet/for/aetest?text=hello'")
status = st.write("Status: " + my_text)

for dweet in dweepy.listen_for_dweets_from('aetest'):
    my_text = dweet["content"]["text"]
    status.write("Status: " + my_text)
    

