import streamlit as st
import requests

@st.cache_data
def fetch_all_kb(update_trigger = st.session_state.get('update_trigger')):
    print("trying to fetch latest kb list from server")
    response = requests.get("http://127.0.0.1:8000/knowledgebase/")
    items = response.json()
    return items

@st.cache_data
def fetch_all_kb_names(update_trigger = st.session_state.get('update_trigger')):
    print("inside fetch all kb names")
    items = fetch_all_kb(st.session_state.get('update_trigger'))
    dict ={item['name']:item['id'] for item in items}
    return dict

def create_kb_and_upload_file(inputs, docs):
    create_kb_response = create_kb(inputs = inputs)
    if create_kb_response.status_code == 201:
        data = create_kb_response.json()
        kb_id = data["kb_id"]
        print(f"received knowledge base id: {kb_id}")
        response = upload_file(kb_id=kb_id, docs=docs)
    return response

def upload_file(kb_id: int, docs):
    files = [('files', (doc.name, doc, 'application/octet-stream')) for doc in docs] if docs else []
    response = requests.post("http://127.0.0.1:8000/knowledgebase/{}/upload/".format(kb_id), files=files)
    return response

def create_kb(inputs):
    response =  requests.post("http://127.0.0.1:8000/knowledgebase/", json=inputs)
    return response

def get_kb_detail(kb_id: int):
    kb =  requests.get("http://127.0.0.1:8000/knowledgebase/{}".format(kb_id))
    files = requests.get("http://127.0.0.1:8000/knowledgebase/{}/files/".format(kb_id))
    return kb, files

def delete_files(ids):
    for id in ids:
        response = requests.delete("http://127.0.0.1:8000/knowledgebasefile/{}".format(id))

def delete_kb(kb_id: int):
    response = requests.delete("http://127.0.0.1:8000/knowledgebase/{}".format(kb_id))