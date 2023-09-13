import streamlit as st

st.set_page_config(
    page_title="Andi's Langchain Projects",
    page_icon="👋",
    # layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.write("# Andi's Langchain Projects 🤖")

st.sidebar.title('AI Toolbox')  
st.sidebar.text('Select a project:')  
st.sidebar.image('files/gitarren.jpeg')

st.markdown(
    """
    &nbsp;
    
    ### This is my Playground for ChatGPT and Langchain projects  
    &nbsp;
    
    **👈 Select a project from the sidebar**  
    &nbsp;
    
    &nbsp;

    The code is hosted on [github](https://github.com/ajerni/erni-langchain)
    """
)
