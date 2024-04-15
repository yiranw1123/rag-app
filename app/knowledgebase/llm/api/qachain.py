from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class QAChain(object):
    __chain = None

    @classmethod
    def get_chain(cls, retriever):
        if cls.__chain is None:
            # Prompt template
            template = """Answer the question based only on the following context, which can include text and tables:
            {context}
            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)

            # Option 1: LLM
            model = ChatOpenAI(temperature=0, model="gpt-4")

                # RAG pipeline
            cls.__chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | model
                | StrOutputParser()
            )

        return cls.__chain