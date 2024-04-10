from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

class Summarizer(object):
    __summarize_chain = None

    @classmethod
    def get_summarize_chain(cls):
        if cls.__summarize_chain is None:
            #Prompt
            prompt_text = """ Summarize the following text: {element} """
            prompt = ChatPromptTemplate.from_template(prompt_text)

            # Summary chain
            model = ChatOllama(temperature=0, model="llama2:13b-chat")
            cls.__summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
        return cls.__summarize_chain

def get_summarizer_chain():
    return Summarizer.get_summarize_chain()