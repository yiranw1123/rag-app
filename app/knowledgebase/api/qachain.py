from langchain.chains import create_history_aware_retriever
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import message_to_dict
from langchain_core.output_parsers import JsonOutputParser

import uuid
import json

class UUIDAwareRedisChatMessageHistory(RedisChatMessageHistory):
    def __init__(self, session_id, url='redis://localhost:6379/', key_prefix="message_store:", ttl=None):
        # Call the parent class's constructor
        super().__init__(session_id, url, key_prefix, ttl)

    def add_message(self, message):
        # Generate a unique message ID
        message_id = str(uuid.uuid4())
        # Include the UUID in the message data, checking if 'id' already exists to avoid overwriting it
        message_dict = message_to_dict(message)

        message_dict['data']['id'] = message_id
        # Serialize the message data with the ID to JSON
        # Safely serialize the message dictionary to JSON
        try:
            serialized_message = json.dumps(message_dict)
        except TypeError as e:
            # Log and handle non-serializable objects
            print(f"Error serializing message: {e}")
            raise
        # Push this message onto the Redis list for this session
        self.redis_client.lpush(self.key, serialized_message)# Return the message ID for reference if needed

class QAChain(object):
    __chain = None

    @classmethod
    def get_chain(cls, retriever):
        if cls.__chain is None:
            llm = ChatOpenAI(temperature=0, model="gpt-4")
            contextualize_q_system_prompt = """Given a chat history and the latest user question \
            which might reference context in the chat history, formulate a standalone question \
            which can be understood without the chat history. Do NOT answer the question, \
            just reformulate it if needed and otherwise return it as is."""
            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
            history_aware_retriever = create_history_aware_retriever(
                llm, retriever, contextualize_q_prompt
            )

            qa_system_prompt = """You are an assistant for question-answering tasks. \
            Use the following pieces of retrieved context to answer the question. \
            If you don't know the answer, just say that you don't know. \
            Use three sentences maximum and keep the answer concise.\

            {context}"""
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )

            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

            def get_session_history(session_id: str) -> UUIDAwareRedisChatMessageHistory:
                return UUIDAwareRedisChatMessageHistory(session_id, url="redis://localhost:6379")
            
            parser = JsonOutputParser()

            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )
        return conversational_rag_chain