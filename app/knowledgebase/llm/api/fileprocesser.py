from unstructured.partition.auto import partition_pdf
from ...constants import IMG_DIRECTORY, UPLOADED_FILES_DIR, COLLECTION_PREFIX
import subprocess
from ...schemas import Element
import glob
import os
from fastapi import UploadFile
import uuid
from ..store.ChromaStore import add_to_collection
from ..store.RedisDocStore import mset
import shutil
from .unstructured_parser import get_raw_pdf_elements, categorize_elements, summarize_imgs

async def summarize_elements(elements, summarize_chain):
    # Apply to text
    texts = [i.text for i in elements]
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})

    return text_summaries

async def store_and_process_file(file:UploadFile, file_id: uuid, kb_id:int, summarizer, chroma_client, redis_client):
    stored_file_name = await save_file(file, file_id)
    print(f"Successfully saved file {file.filename} to directory")
    raw_pdf_elements = await get_raw_pdf_elements(filename=stored_file_name, img_dir=f"{IMG_DIRECTORY}{file_id}/")
    table_elements, text_elements = await categorize_elements(raw_pdf_elements)
    print(f"File {file.filename} has {len(table_elements)} tables and {len(text_elements)} texts")

    collection_name = f"{COLLECTION_PREFIX}{str(kb_id)}"
    redis_namespace = f"{collection_name}:{file_id}"


    text_summaries = await summarize_elements(text_elements, summarizer)
    doc_ids = add_to_collection(text_summaries, file_id, collection_name, chroma_client)
    await mset(redis_namespace, doc_ids, [text_element.text for text_element in text_elements], redis_client)
    print(f"processed {len(text_summaries)} text summaries")

    if len(table_elements) > 0:
        table_summaries= await summarize_elements(table_elements, summarizer)
        table_ids = add_to_collection(table_summaries, file_id, collection_name, chroma_client)
        await mset(redis_namespace, table_ids, [table_element.text for table_element in table_elements],redis_client)
        print(f"processed {len(table_summaries)} table summaries")

    if len(os.listdir(f"{IMG_DIRECTORY}{file_id}")) != 0:
        img_summaries = await summarize_imgs(file_id=file_id)
        print(f"processed {len(img_summaries)} image summaries")
        img_ids = add_to_collection(img_summaries, file_id, collection_name, chroma_client)
        await mset(redis_namespace, img_ids, img_summaries,redis_client)
        print("Added image summary to collection")
        await clear_img_dir(file_id=file_id)
    
    await clear_file_dir(file_id=file_id)


async def save_file(file:UploadFile, file_id: uuid):
    file_dir = f"{UPLOADED_FILES_DIR}{file_id}/"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    try:
        contents = file.file.read()
        _, file_ext = os.path.splitext(file.filename)
        stored_file_name = f"{file_id}{file_ext}"
        with open(file_dir+stored_file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        f.close()
        file.file.close()
        return f"{file_dir}{stored_file_name}"

async def clear_file_dir(file_id:str):
    shutil.rmtree(f"{UPLOADED_FILES_DIR}{file_id}")

async def clear_img_dir(file_id:str):
    shutil.rmtree(f"{IMG_DIRECTORY}{file_id}")
    
