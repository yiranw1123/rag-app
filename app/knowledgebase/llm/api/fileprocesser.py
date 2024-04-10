from unstructured.partition.auto import partition_pdf
from ...constants import IMG_DIRECTORY, UPLOADED_FILES_DIR
import subprocess
from ...schemas import Element
import glob
import os
from fastapi import UploadFile
import uuid

async def summarize_elements(elements, summarize_chain):
    # Apply to text
    texts = [i.text for i in elements]
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})

    return text_summaries

async def store_and_process_file(file:UploadFile, file_id: uuid, summarizer):
    stored_file_name = await save_file(file, file_id)
    print(f"Successfully saved file {file.filename} to local directory")
    await clear_img_dir()
    print("Cleared image directory for unstructured pdf parsing")
    raw_pdf_elements = await get_raw_pdf_elements(filename=stored_file_name)
    table_elements, text_elements = await categorize_elements(raw_pdf_elements)
    print(f"File {file.filename} has {len(table_elements)} tables and {len(text_elements)} texts")
    text_summaries = await summarize_elements(text_elements, summarizer)
    table_summaries= await summarize_elements(table_elements, summarizer)
    if len(os.listdir(IMG_DIRECTORY)) != 0:
        img_summaries = await summarize_imgs()
        print(f"processed {len(img_summaries)} image summaries")
    print(f"processed {len(text_summaries)} text summaries, {len(table_summaries)} table summaries")

async def save_file(file:UploadFile, file_id: uuid):
    if not os.path.exists(UPLOADED_FILES_DIR):
        os.makedirs(UPLOADED_FILES_DIR)
    try:
        contents = file.file.read()
        _, file_ext = os.path.splitext(file.filename)
        stored_file_name = f"{file_id}{file_ext}"
        with open(UPLOADED_FILES_DIR+stored_file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        f.close()
        file.file.close()
        return stored_file_name
    
async def clear_img_dir():
    for file in os.listdir(IMG_DIRECTORY):
        os.remove(f"{IMG_DIRECTORY}{file}")
    
async def get_raw_pdf_elements(filename):
    print("received file {}, ready to parse using unstructured".format(filename))
    return partition_pdf(
        filename=UPLOADED_FILES_DIR + filename,
        # Using pdf format to find embedded image blocks
        extract_images_in_pdf=True,
        # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
        # Titles are any sub-section of the document
        infer_table_structure=True,
        # Post processing to aggregate text once we have the title
        chunking_strategy="by_title",
        # Chunking params to aggregate text blocks
        # Attempt to create a new chunk 3800 chars
        # Attempt to keep chunks > 2000 chars
        # Hard max on chunks
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        content_type="application/octet-stream",
        image_output_dir_path=IMG_DIRECTORY,
    )

async def categorize_elements(raw_pdf_elements):

    # Create a dictionary to store counts of each type
    category_counts = {}

    for element in raw_pdf_elements:
        category = str(type(element))
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    # Categorize by type
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", text=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    # Tables
    table_elements = [e for e in categorized_elements if e.type == "table"]
    # Text
    text_elements = [e for e in categorized_elements if e.type == "text"]

    return table_elements, text_elements

async def summarize_imgs():
    #summarize imgs
    subprocess.call(['sh', "summarize_img.sh"])

    # Get all .txt files in the directory
    file_paths = glob.glob(os.path.expanduser(os.path.join(IMG_DIRECTORY, "*.txt")))

    print("Found ", len(file_paths), "imgs in directory")

    # Read each file and store its content in a list
    img_summaries = []
    for file_path in file_paths:
        file = open(file_path, "r")
        doc = ""
        for line in file:
            if line.startswith("clip_model_load") or line.startswith("encode_image_with_clip"):
                continue
            else:
                doc += line
        img_summaries.append(doc)
    
    print("Processed ", len(img_summaries), " summaries from directory.")
    
    return img_summaries
