from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from .. import schemas
from ..routers import chatmessage, tags
from sentence_transformers import SentenceTransformer
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from typing import List
import numpy as np


# Instantiate model once
model = SentenceTransformer('all-miniLM-L6-v2')

async def process_and_get_answer(kb_id, id, data, retriever, db):
    # get response object res from llm
    res = await get_resp_from_retriever(id, retriever, data)
    # embed question
    question_embedding = await get_embedding(res['input'])
    #create context dictionary
    pydantic_docs = schemas.DocumentList(documents = [schemas.Document(page_content=document.page_content, doc_id=document.metadata['doc_id']) for document in res['context']])

    context_dict = pydantic_docs.model_dump()

    # base createchatmessage
    base_message = schemas.CreateChatMessage(chatId = id, question=res['input'], answer=res['answer'],
                                              sources=context_dict, embedding = question_embedding)

    # get tag for question
    # update chat message with created tags
    tags_dict = await get_keywords(kb_id, base_message, db)

    base_message.tags = tags_dict
    # save tag to tags db
    message = await chatmessage.create(base_message, db)
    return message


async def get_keywords(kb_id, base_message: schemas.CreateChatMessage, db):
    prompt = PromptTemplate.from_template(f"""
        Given the following information:
        User Question: {{question}}
        Answer Provided: {{answer}}
        Context: {{context}}

        Based on the user's intent derived from the question, answer, and context, identify two key aspects or keywords. Format your response as a single line of text with the keywords separated by a comma. No additional text or explanation is needed.

        Example of desired output: "keyword1, keyword2"
        """
    )
    model = ChatOpenAI(temperature=0, model="gpt-4")
    parser =  CommaSeparatedListOutputParser()
    chain = prompt | model | parser
    input = {"question":base_message.question, 
            "answer": base_message.answer, 
            "context":base_message.sources}
    # list of keywords
    keywords = await chain.ainvoke(input)
    #dict:{'matches':[schemas.Tag],
    #      'new_tags':[schemas.CreateTag]}
    tags_dict = await create_and_merge_keywords(kb_id, keywords, db)
    return tags_dict

async def create_and_merge_keywords(kb_id, texts:List[str], db):
    # Convert list of strings to list of Tag models
    # schema.CreateTag
    new_tags=[schemas.CreateTag(text=tag, embedding = await get_embedding(tag)) for tag in texts]
    # schemas.Tag
    retrieved_tags = await tags.get_by_kbid(kb_id, db)
    new_embeddings = np.array([tag.embedding for tag in new_tags])

    merged_tags =[]
    # Prepare results structure
    results = {
        'matches': [],
        'new_tags': []
    }

    if retrieved_tags:

        # Prepare existing embeddings
        existing_embeddings = np.array([tag.embedding for tag in retrieved_tags])

        # Compute similarities using a vectorized operation
        similarities = np.dot(new_embeddings, existing_embeddings.T)

        # Determine matches based on a similarity threshold
        threshold = 0.9
        matched_indices = set()
        for i, new_tag in enumerate(new_tags):
            max_similarity_index = np.argmax(similarities[i])
            max_similarity = similarities[i][max_similarity_index]

            if max_similarity > threshold:
                # Record the index of the existing tag that matches and the new tag
                matched_indices.add(max_similarity_index)
                results['matches'].append(retrieved_tags[max_similarity_index])
            else:
                # List this tag as needing to be created
                results['new_tags'].append(new_tag)
    else:
        results['new_tags'] = new_tags
    
    return results


async def get_resp_from_retriever(id, retriever, msg):
    res = await retriever.ainvoke(
        {"input": msg},
        config={
            "configurable": {"session_id":id}
        })
    return res

async def get_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()