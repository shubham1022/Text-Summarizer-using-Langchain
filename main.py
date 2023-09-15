import os
import openai
import streamlit as st
from langchain import PromptTemplate
from langchain import OpenAI

openai.api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title="Text Summarizer", page_icon=":robot:")
st.header("Text Summarizer")

from langchain import FewShotPromptTemplate

# create our examples
examples = [
    {
        "query": "summarize the below text in 20 words:The first decade of the 20th century saw increasing diplomatic tension between the European great powers. This reached a breaking point on 28 June 1914, when a Bosnian Serb named Gavrilo Princip assassinated Archduke Franz Ferdinand, heir to the Austro-Hungarian throne. Austria-Hungary held Serbia responsible, and declared war on 28 July. Russia came to Serbia's defence, and by 4 August, Germany, France and Britain were drawn into the war, with the Ottoman Empire joining in November the same year.",
        "answer": "In the early 20th century, rising tensions led to WWI after Archduke's assassination in 1914, involving major European powers."
    }, {
        "query": "summarize the below text in 30 words:German strategy in 1914 was to first defeat France then transfer forces to the Russian front. However, this failed, and by the end of 1914, the Western Front consisted of a continuous line of trenches stretching from the English Channel to Switzerland. The Eastern Front was more dynamic, but neither side could gain a decisive advantage, despite costly offensives. As the war expanded to more fronts, Bulgaria, Romania, Greece, Italy and others joined in between 1915 and 1917. In early 1917, the United States entered the war on the side of the Allies, while in late 1917, the Bolsheviks seized power in the Russian October Revolution and made peace with the Central Powers in early 1918.",
        "answer": "In 1914, Germany aimed to defeat France and later shift to the Russian front, but this plan failed. By the end of 1914, the Western Front featured trench warfare. The Eastern Front saw ongoing battles, and new countries joined the war until 1917. The US joined the Allies in early 1917, and the Russian October Revolution led to peace with the Central Powers in early 1918."

    }
]

# create a example template
example_template = """
User: {query}
AI: {answer}
"""

# create a prompt example from above template
example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

# now break our previous prompt into a prefix and suffix
# the prefix is our instructions
prefix = """You are a Text Summarizer bot,
 your task is to generate summary of the given text only. Other than that you are not allowed to give any queries answer.
 Do not generate summary for less than 100 words paragraph, if you getting less than 100 words paragraph for summarizer task, 
 you will have to reply: I am sorry, kindly give a paragraph more than 100 words.
"""
# and the suffix our user input and output indicator
suffix = """
User: {query}
AI: """

# now create the few shot prompt template
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n"
)


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

summary_input = get_text()

st.markdown("#### Summary")

if summary_input:
    prompt_summary = few_shot_prompt_template.format(query=summary_input)   
    formatted_summary = llm(prompt_summary)
    st.write(formatted_summary)



