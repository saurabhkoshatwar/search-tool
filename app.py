import streamlit as st
import json

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Initialize session state for search query and previous selection if not exists
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'previous_selection' not in st.session_state:
    st.session_state.previous_selection = None

# Sidebar: dynamic search options for each top-level key
st.sidebar.markdown("""
    <h2 style='color:#4F8BF9; margin-bottom:0.5em;'>Search Option</h2>
    <p style='color:#888; margin-top:0;'>Choose a category to search:</p>
""", unsafe_allow_html=True)

# Use radio with icons for better appearance and state management
category_labels = [f"🔍 {key}" for key in data.keys()]
category_map = dict(zip(category_labels, data.keys()))
selected_label = st.sidebar.radio(
    label="",
    options=category_labels,
    index=0,
    key="category_radio"
)
selected_key = category_map[selected_label]

# Reset search query when sidebar selection changes
if st.session_state.previous_selection != selected_key:
    st.session_state.search_query = ""
    st.session_state.previous_selection = selected_key

# Get the items for the selected category
items = data[selected_key]

# Search box - preserve query across selections
search_query = st.text_input(
    f"Search in {selected_key}", 
    value=st.session_state.search_query,
    key=f"search_{selected_key}"
)

# Update session state when search query changes
if search_query != st.session_state.search_query:
    st.session_state.search_query = search_query

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