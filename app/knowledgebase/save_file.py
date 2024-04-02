import os
from fastapi import UploadFile
from .constants import UPLOADED_FILES_DIR

def save_file(file:UploadFile):
    if not os.path.exists(UPLOADED_FILES_DIR):
        os.makedirs(UPLOADED_FILES_DIR)
    try:
        contents = file.file.read()
        with open(UPLOADED_FILES_DIR+f'{file.filename}', 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        f.close()
        file.file.close()