import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.utilities import GoogleSerperAPIWrapper

# from langchain.agents import load_tools, initialize_agent, AgentType

import os
import pprint

os.environ["SERPER_API_KEY"] = st.secrets["serper_api_key"]

llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets["openai_api_key"])

st.header(
    """
:blue[Andi's Streamlit-Langchain-Food-Bot]
"""
)

# st.markdown("![kaze](https://upload.wikimedia.org/wikipedia/commons/1/15/Cat_August_2010-4.jpg)")

my_country = st.text_input("Enter country")

template = """
let me know a typical meal from {country}.
Respond in one short sentence.
"""

prompt = PromptTemplate(
    input_variables=["country"],
    template=template,
)

final_prompt = prompt.format(country=my_country)

if my_country:

    result = llm(final_prompt)

    st.write(":blue[Here comes a typical meal of the country you entered:]")

    st.write(result)

    if result:
        search = GoogleSerperAPIWrapper(type="images", num=1)
        image_result = search.results(result)
        pprint.pp(image_result)  # just to display it properly in the terminal

        # who needs a json parser etc. :-) English is my new preferred programming language :-) / Still learn and understand the output parsers of langchain!!!
        img_template = """
        Look through this data {img_json} and find the first hyperlink that ends with .jpg under 'imgUrl' entry. Reply with that hyperlink only. No other text in the reply.
        """

        img_template_prompt = PromptTemplate(
            input_variables=["img_json"],
            template=img_template,
        )

        img_template_prompt_final = img_template_prompt.format(img_json=image_result)

        link_to_image = llm(img_template_prompt_final)

        st.write(link_to_image)

        st.image(link_to_image, width=250)
