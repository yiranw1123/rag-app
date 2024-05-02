from unstructured.partition.auto import partition_pdf
from ..constants import IMG_DIRECTORY
import subprocess
from ..schemas import Element
import glob
import os
import re

async def get_raw_pdf_elements(filename, img_dir):
    print("received file {}, ready to parse using unstructured".format(filename))
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    
    return partition_pdf(
        filename=filename,
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
        extract_image_block_types=["Image", "Table"],          # optional
        extract_image_block_to_payload=False,                  # optional
        extract_image_block_output_dir=img_dir,
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

async def summarize_imgs(file_id:str):
    params = [str(file_id)]
    #summarize imgs
    subprocess.call(['sh', "summarize_img.sh"]+params)

    # Get all .txt files in the directory
    file_paths = glob.glob(os.path.expanduser(os.path.join(f"{IMG_DIRECTORY}{file_id}", "*.txt")))

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
    
    print("Processed ", len(img_summaries), " image summaries from directory.")
    
    return img_summaries