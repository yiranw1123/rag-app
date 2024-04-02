import streamlit as st
from st_pages import add_indentation
from api import fetch_all_kb_names, get_kb_detail, delete_files,delete_kb
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout = "wide")

def files_df_buttons():
    col1, col2, col3 = st.columns([1,1.5,1.5])
    with col1:
        if st.button("Delete all", key = "del_all"):
            cols = st.session_state.df.columns
            st.session_state.df = pd.DataFrame(columns = cols)
            st.success("Data deleted.")
    with col2:
        if st.button("Delete Selected", key = "save_to_db"):
            selected_ids = []
            for k, v in st.session_state.files_df["edited_rows"].items():
                selected_ids.append(files_df.iloc[k]['id'])
            delete_files(selected_ids)
            st.session_state.df = files_df.loc[files_df["selected"] != True]
    with col3:
        if st.button("Add File"):
            switch_page("Manage_Knowledgebases")

if 'update_trigger' not in st.session_state:
    st.session_state.update_trigger = 0

kb_cols = ["id", "name", "embedding", "created", "updated"]
cols = ["file_name", "created", "updated", "selected"]
add_indentation()

data = fetch_all_kb_names(st.session_state.get('update_trigger'))

if not data:
    st.markdown("Please create a knowledge base to proceed.")
    empty_df = pd.DataFrame(columns = cols)
    st.data_editor(empty_df, use_container_width= True)
    st.session_state.df = empty_df
    st.session_state.full = empty_df.copy()

else:
    kb = st.selectbox("Select a KnowledgeBase to view", data.keys())
    kb_id = data[kb]

    kb, files = get_kb_detail(kb_id)
    kb_details = kb.json()
    df = pd.DataFrame([kb_details])
    df = df.set_index('id')
    
    if not df.empty:
        df["selected"] =[False for i in range(df.shape[0])]
    else:
        df = pd.DataFrame(columns = kb_cols)

    files_df = pd.DataFrame(files.json())
    if not files_df.empty:
        files_df["selected"] =[False for i in range(files_df.shape[0])]
    else:
        files_df = pd.DataFrame(columns = cols)

    st.session_state.df = pd.DataFrame(columns = files_df.columns)
    st.session_state.full = files_df.copy()

    with st.container():
        st.subheader("Showing details for Knowledgebase :blue[{}]".format(kb_details["name"]))
        st.data_editor(df, use_container_width= True)
        st.subheader("Files")
        st.data_editor(files_df, num_rows = "dynamic", use_container_width= True, key="files_df",\
                    column_order = ("file_name", "created", "updated", "selected"),\
                    column_config = {"selected": st.column_config.CheckboxColumn("selected", default = False)})
        files_df_buttons()