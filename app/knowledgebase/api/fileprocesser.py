from ..constants import IMG_DIRECTORY, UPLOADED_FILES_DIR
import os
from fastapi import UploadFile
import uuid
import shutil
from .unstructured_parser import get_raw_pdf_elements, categorize_elements, summarize_imgs
import logging

logger = logging.getLogger(__name__)

async def summarize_elements(elements, summarize_chain):
    # Apply to text
    texts = [i.text for i in elements]
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})

    return text_summaries

async def save_file(file:UploadFile, file_id: uuid):
    stored_file_name = await save_file(file, file_id)
    print(f"Successfully saved file {file.filename} to directory")
    return stored_file_name


async def parse_pdf(stored_file_name: str, file_id: uuid):
    raw_pdf_elements = await get_raw_pdf_elements(filename=stored_file_name, img_dir=f"{IMG_DIRECTORY}{file_id}/")
    table_elements, text_elements = await categorize_elements(raw_pdf_elements)
    print(f"File has {len(table_elements)} tables and {len(text_elements)} texts")
    return table_elements, text_elements

async def summarize(text_elements, table_elements, file_id, summarizer):
    text_summaries = await summarize_elements(text_elements, summarizer)
    table_summaries= await summarize_elements(table_elements, summarizer) if len(table_elements) >0 else []
    img_summaries = await summarize_imgs(file_id=file_id) if len(os.listdir(f"{IMG_DIRECTORY}{file_id}")) != 0 else []
    return text_summaries, table_summaries, img_summaries

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
    
