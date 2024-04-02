import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from api import fetch_all_kb
from st_pages import add_indentation
import math

st.set_page_config(layout = "wide")
if 'update_trigger' not in st.session_state:
    st.session_state.update_trigger = 0

def split_frame(data, rows):
    return [data[i:i + rows] for i in range(0, len(data), rows)]

def paginate_data(data):
    pagination = st.container()
    bottom_menu = st.columns((4,1,1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[5,10,20])
    with bottom_menu[1]:
        total_pages = (
            int(math.ceil(len(data) / batch_size)) if int(len(data)/ batch_size) > 0 else 1
        )
        current_page = st.selectbox("Page", [i for i in range(1, total_pages+1)])
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page} ** of **{total_pages}** ")

    pages = split_frame(data, batch_size)
    return pagination.dataframe(data = pages[current_page - 1], use_container_width = True)
    
add_indentation()

st.title("KnowledgeBase")

if st.session_state.update_trigger >= 0:
    data = fetch_all_kb(st.session_state.get('update_trigger'))

    st.write(data)
    if not data:
        if st.button('Add a KnowledgeBase'):
            switch_page('Manage_Knowledgebases')
    else:
        paginate_data(data=data)

        if st.button("View KnowledgeBase"):
            switch_page("View_Knowledgebases")