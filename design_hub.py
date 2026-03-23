import streamlit as st
import sqlite3
import os # NEW: Add this to the top of your file

# --- Folder Setup ---
# Create an images directory if it doesn't exist yet
if not os.path.exists("images"):
    os.makedirs("images")

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
            
    # ... (Keep the 'Draft a new prompt' section exactly the same) ...
    
    st.divider()
    
    # --- UPDATED: Display saved prompts with Delete buttons ---
    st.subheader("Your Saved Prompts")
    c = conn.cursor()
    # Notice we are now selecting the 'id' as well as the text
    c.execute('SELECT id, prompt_text FROM prompts ORDER BY id DESC')
    saved_prompts = c.fetchall()
    
    if saved_prompts:
        for prompt_id, prompt_text in saved_prompts:
            # Create two columns: a wide one for the code, a narrow one for the button
            col1, col2 = st.columns([5, 1]) 
            
            with col1:
                st.code(prompt_text, language="plaintext")
            
            with col2:
                # We use the unique database ID to give each button a unique Streamlit key!
                if st.button("Delete", key=f"delete_{prompt_id}"):
                    c.execute('DELETE FROM prompts WHERE id = ?', (prompt_id,))
                    conn.commit()
                    st.rerun() # This instantly refreshes the page so the prompt disappears
    else:
        st.info("No prompts saved yet.")

# --- TAB 3: Reference Gallery (Updated) ---
with tab3:
    st.header("Reference Gallery")
    st.write("Upload layouts or inspiration images to save them locally.")
    
    # 1. The Uploader
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview", use_container_width=True)
        
        # 2. The Save Button
        if st.button("Save to Gallery"):
            # Construct the file path (e.g., "images/my_layout.png")
            file_path = os.path.join("images", uploaded_file.name)
            
            # Write the file to the images folder
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Saved {uploaded_file.name} permanently!")
            
    st.divider()
    
    # 3. Displaying the Saved Gallery
    st.subheader("Saved References")
    
    # Get a list of all files in the images folder
    saved_images = os.listdir("images")
    
    if saved_images:
        # Create a grid layout (3 columns) for the gallery
        cols = st.columns(3)
        for index, image_name in enumerate(saved_images):
            # Display images in a grid by calculating which column to use
            with cols[index % 3]:
                img_path = os.path.join("images", image_name)
                st.image(img_path, caption=image_name, use_container_width=True)
    else:
        st.info("Your gallery is empty. Upload an image above to get started!")
