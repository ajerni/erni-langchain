import streamlit as st
from langchain import LLMMathChain, LLMChain
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.utilities import GoogleSerperAPIWrapper

import os
os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

st.header(
    """
:blue[Andi's Agent Demo - find the codeword "code123"]
"""
)

my_entry = st.text_input("Enter a question (maybe including a calculation) and/or the magic code...")

def my_own_function(argreceived):
    """returns a string when the magic code code123 was mentioned in the search"""
    print('...at least reached it...')
    print(argreceived)
    #this return is treated as a prompt to llm again!!!
    return "Give the following final Answer as an unchanged string: 'You found the magic code. Congratulations!'"
    #return "tell me a joke about chicken"

search = GoogleSerperAPIWrapper(serper_api_key=st.secrets["serper_api_key"])
llm_math_chain = LLMMathChain(llm=llm, verbose=True)
gpt_llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets["openai_api_key"])

tools = [
    Tool.from_function(
        func=gpt_llm,
        name="gpt",
        description="useful for when you need to answer questions about listing, summarization, categorization and any other tasks that ChatGPT can typically solve. Do not use this tool when the questions contains 'code123'"
    ),
    Tool.from_function(
        func=search.run,
        name="Search",
        description="useful for when you need to answer questions about current events or any general search. Do not use this tool when the questions contains 'code123'"
    ),
    Tool.from_function(
        func=llm_math_chain.run,
        name="Calculator",
        description="useful for when you need to answer questions about math. Do not use this tool when the questions contains 'code123'"
    ),
    Tool.from_function(
        func=my_own_function,
        name="code123",
        description="This is all your knowledge about code123. Use this tool whenever you see 'code123' mentioned somewhere. Disregard any ohter context whenever code123 is mentioned."
    ),
]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if my_entry:
    response = agent.run(my_entry)
    print(response)
    st.write(response)
