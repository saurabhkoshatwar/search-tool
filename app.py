import streamlit as st
import json

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Sidebar: dynamic search options for each top-level key
st.sidebar.title('Search Option')

# Use buttons with search icon for each category
selected_key = None
for key in data.keys():
    if st.sidebar.button(f'🔍 {key} search'):
        selected_key = key

# Default to the first key if none selected (on first load)
if selected_key is None:
    selected_key = list(data.keys())[0]

# Get the items for the selected category
items = data[selected_key]

# Search box
search_query = st.text_input(f"Search in {selected_key}", "")

# Filter items based on search query (case-insensitive, in name or description)
def filter_items(items, query):
    if not query:
        return items.items()
    query = query.lower()
    return [
        (name, desc)
        for name, desc in items.items()
        if query in name.lower() or query in desc.lower()
    ]

filtered_items = filter_items(items, search_query)

# Main section: show results
st.header(f"{selected_key} List")
if filtered_items:
    for name, desc in filtered_items:
        st.markdown(
            f"""
            <div style='margin-bottom: 1.2em;'>
                <span style='font-size:1.5em; font-weight:700; color:var(--text-color);'>{name}:</span>
                <span style='font-size:1.15em; color:var(--text-color-secondary);'>{desc}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No results found.") 