import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
import os

df = pd.read_csv("files/auto.csv")

os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]

agent = create_pandas_dataframe_agent(OpenAI(model_name="gpt-3.5-turbo"), df, verbose=True)

st.header("Querying structured data")

input_q = st.text_input("Ask question to the CSV file")

result = agent.run(input_q)

st.write(result)

