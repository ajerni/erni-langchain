import streamlit as st
import base64


# Function to set Image as Background (or any other general CSS settings i.e. color: white etc.)
def add_local_backgound_image_(image):
    with open(image, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    # st.write("Image Courtesy: andierni")
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:files/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        color: white
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


st.write("Background Image")
st.markdown("All code available on [github](https://github.com/ajerni/erni-langchain)")

# Calling Image in function
add_local_backgound_image_("files/bg.png")
