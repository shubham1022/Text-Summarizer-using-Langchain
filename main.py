
import os
import openai
import streamlit as st
from langchain import PromptTemplate
from langchain import OpenAI

openai.api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title="Professional Email", page_icon=":robot:")
st.header("Professional Email")


template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

# The line `prompt = PromptTemplate(input_variables={'tone','dialect','email'}, template=template)` is
# creating an instance of the `PromptTemplate` class.
prompt = PromptTemplate(input_variables={'tone','dialect','email'}, template=template)

def load_llm():
    """
    The function `load_llm` loads the OpenAI language model with a specified temperature and API key.
    
    :param openai_api_key: The `openai_api_key` parameter is the API key provided by OpenAI. It is used
    to authenticate and authorize access to the OpenAI API. You can obtain an API key by signing up for
    an account on the OpenAI website and following the instructions to generate an API key
    :return: an instance of the OpenAI class with a temperature of 0.5 and the provided OpenAI API key.
    """
    llm = OpenAI(temperature=.5)
    return llm

llm = load_llm()

# def get_api_key():
#     input_text = st.text_input(label="openai_api_key",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
#     return input_text

# openai_api_key = get_api_key()



col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format. This tool \
                is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
                [@GregKamradt](https://twitter.com/GregKamradt). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")
    
st.markdown("### Enter Your Email To Convert")

col1, col2 = st.columns(2)

with col1:
    option_tone = st.selectbox(
        "Which tone would you like your email to have?",
        ('Formal','Informal'))
    
with col2:
    option_dialect = st.selectbox(
        "Which english dialect would you like?",('American','British'))    
    
def get_text():
    input_text = st.text_area(label="Email Input",placeholder="your email...", key="email_input")
    return input_text 

email_input = get_text()

st.markdown("### Your Converted Email")

if email_input:
    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)
   
    formatted_email = llm(prompt_with_email)
    st.write(formatted_email)



