import streamlit as st
import sqlite3

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('design_assets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_text TEXT
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

# Set up the page
st.set_page_config(page_title="Design Organizer", page_icon="🎨", layout="centered")
st.title("🎨 Design Asset & Prompt Organizer")
st.markdown("A centralized hub for graphic assets, colors, and generator prompts.")

tab1, tab2, tab3 = st.tabs(["🎨 Brand Colors", "📝 Prompt Library", "🖼️ Layout References"])

# --- TAB 1: Brand Colors ---
with tab1:
    st.header("Color Palette")
    st.write("Save your most used hex codes here.")
    
    col1, col2 = st.columns(2)
    with col1:
        color1 = st.color_picker("Primary Color", "#1E88E5")
        st.code(color1, language="plaintext")
    with col2:
        color2 = st.color_picker("Accent Color", "#D81B60")
        st.code(color2, language="plaintext")

# --- TAB 2: Prompt Library ---
with tab2:
    st.header("Generator Prompts")
    
    new_prompt = st.text_area(
        "Draft a new prompt:", 
        placeholder="e.g., Safari theme tarpaulin background, cute jungle animals, pastel green and gold, high resolution"
    )
    
    # We only have ONE "Save Prompt" button now!
    if st.button("Save Prompt"):
        if new_prompt:
            c = conn.cursor()
            c.execute('INSERT INTO prompts (prompt_text) VALUES (?)', (new_prompt,))
            conn.commit()
            st.success("Prompt saved to database!")
        else:
            st.warning("Please enter a prompt before saving.")
            
    st.divider()
    
    st.subheader("Your Saved Prompts")
    c = conn.cursor()
    c.execute('SELECT prompt_text FROM prompts ORDER BY id DESC')
    saved_prompts = c.fetchall()
    
    if saved_prompts:
        for prompt in saved_prompts:
            st.code(prompt[0], language="plaintext")
    else:
        st.info("No prompts saved yet.")

# --- TAB 3: Reference Gallery ---
with tab3:
    st.header("Reference Uploads")
    st.write("Upload layouts or inspiration images.")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Reference", use_container_width=True)
