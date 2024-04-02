from unstructured.partition.auto import partition
from ..knowledgebase.constants import IMG_DIRECTORY, UPLOADED_FILES_DIR
import subprocess
from ..knowledgebase.schemas import Element
import glob
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

def get_raw_pdf_elements(filename):
    print("received file {}".format(filename))
    return partition(
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

def categorize_elements(raw_pdf_elements):

    # Create a dictionary to store counts of each type
    category_counts = {}

    for element in raw_pdf_elements:
        category = str(type(element))
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    print(category_counts)

    # Categorize by type
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", text=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    # Tables
    table_elements = [e for e in categorized_elements if e.type == "table"]
    print("Number of table elements ", len(table_elements))

    # Text
    text_elements = [e for e in categorized_elements if e.type == "text"]
    print("Number of text elements",  len(text_elements))

    return table_elements, text_elements

def summarize_elements(table_elements, text_elements):

    # Prompt
    prompt_text = """ Summarize the following text: {element} """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Summary chain
    model = ChatOllama(temperature=0, model="llama2:13b-chat")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Apply to text
    texts = [i.text for i in text_elements]
    text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})

    # Apply to tables
    tables = [i.text for i in table_elements]
    table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})
    
    return table_summaries, text_summaries, texts, tables


def summarize_imgs(img_path):
    #summarize imgs
    subprocess.call(['sh', "summarize_img.sh"])

    # Get all .txt files in the directory
    file_paths = glob.glob(os.path.expanduser(os.path.join(img_path, "*.txt")))

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

def process_pdf_and_summarize_elements(filename):
    raw_pdf_elements = get_raw_pdf_elements(filename=filename)
    table_elements, text_elements = categorize_elements(raw_pdf_elements)
    table_summaries, text_summaries, texts, tables = summarize_elements(table_elements, text_elements)
    img_summaries = summarize_imgs(IMG_DIRECTORY)
    return table_summaries, text_summaries, img_summaries, texts, tables