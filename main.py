
import os
import openai
import streamlit as st
from langchain import PromptTemplate
from langchain import OpenAI

openai.api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title="Text Summerizer", page_icon=":robot:")
st.header("Text Summerizer")


template =""" Please provide a concise summary of the following text/article/paragraph {text}. Summarize the main points, key arguments, and any important details,
 keeping the summary within limit e.g., 150 words  characters.Ensure that your sole responsibility is to summarize the text; any user queries unrelated to
 text summarization should be declined without further action.

 Your goal is to:
 - Generate the summery of the given text
 YOUR {text} RESPONSE:
"""


prompt = PromptTemplate(input_variables=['text'], template=template)

def load_llm():
    """
    The function `load_llm` returns an instance of the OpenAI language model with a temperature of 0.5.
    :return: The function `load_llm` returns an instance of the OpenAI class with a temperature of 0.5.
    """
    llm = OpenAI(temperature=.5)
    return llm

llm = load_llm()


st.markdown("#### Enter Your Text To Convert")


def get_text():
    input_text = st.text_area(label="",placeholder="your text...", key="text")
    return input_text 

summery_input = get_text()

st.markdown("#### Summery")

if summery_input:
    prompt_summary = prompt.format(text=summery_input)   
    formatted_summary = llm(prompt_summary)
    st.write(formatted_summary)



