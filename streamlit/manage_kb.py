import streamlit as st
from api import fetch_all_kb_names, create_kb_and_upload_file, upload_file, delete_kb
from st_pages import add_indentation

st.set_page_config(layout = "centered")

if 'update_trigger' not in st.session_state:
    st.session_state.update_trigger = 0

add_indentation()

tab1, tab2, tab3 = st.tabs(["Add KnowledgeBase", "File Upload", "Delete Knowledgbase"])
with tab1:
    name = st.text_input("Name")
    description =  st.text_input("Description")
    docs = st.file_uploader("Upload your documents here", accept_multiple_files= True)
    if st.button("Process"):
        with st.spinner("Processing"):
            inputs = {"knowledgebase_name":name, "description":description}
            response = create_kb_and_upload_file(inputs, docs)
            print("Successfully uploaded file")
        print('before update trigger counter: ', st.session_state.update_trigger)
        st.session_state.update_trigger += 1
        print('update trigger counter: ', st.session_state.update_trigger)

with tab2:
    if st.session_state.update_trigger >=0:
        name_id_dict= fetch_all_kb_names(st.session_state.update_trigger)
        if not name_id_dict.keys():
            st.write(":red[Create a KnowledgeBase to continue adding files]")
            option = st.selectbox("Select a KnowledgeBase from List", [])
        else:
            option = st.selectbox("Select a KnowledgeBase from List", name_id_dict.keys())
            kb_id = name_id_dict[option]
    
        docs = st.file_uploader("Upload your documents here",\
                                accept_multiple_files= True, key='file_upload')
        if st.button("Upload"):
            response = upload_file(kb_id=kb_id, docs=docs)

with tab3:
    if st.session_state.update_trigger >=0:
        name_id_dict= fetch_all_kb_names(st.session_state.update_trigger)
        if not name_id_dict.keys():
            st.write(":red[Create a KnowledgeBase to continue adding files]")
            option = st.selectbox("Select a KnowledgeBase from List", [], key = "empty-delete-kb")
        else:
            option = st.selectbox("Select a KnowledgeBase from List", name_id_dict.keys(), key = "delete-kb")
            kb_id = name_id_dict[option]
    if st.button("Delete"):
        st.session_state.update_trigger += 1
        delete_kb(kb_id=kb_id)