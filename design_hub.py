import streamlit as st
import sqlite3
import os
from colorthief import ColorThief

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

tab1, tab2, tab3, tab4 = st.tabs(["🎨 Brand Colors", "📝 Prompt Library", "🖼️ Layout References", "🪄 Color Extractor"])

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
# --- TAB 4: Color Extractor ---
with tab4:
    st.header("🪄 Magic Color Extractor")
    st.write("Upload a design photo or reference image to instantly pull its color palette.")
    
    # Upload the image
    palette_image = st.file_uploader("Upload an image for color extraction", type=["png", "jpg", "jpeg"], key="palette_uploader")
    
    if palette_image is not None:
        # Display the uploaded image
        st.image(palette_image, caption="Analyzing this image...", use_container_width=True)
        
        if st.button("Extract Palette"):
            with st.spinner("Extracting colors..."):
                try:
                    # ColorThief reads the Streamlit uploaded file directly
                    color_thief = ColorThief(palette_image)
                    
                    # Get the top 5 dominant colors (returns a list of RGB tuples)
                    palette = color_thief.get_palette(color_count=5)
                    
                    st.subheader("Extracted Color Hex Codes")
                    
                    # Create 5 columns to display the colors side-by-side beautifully
                    cols = st.columns(len(palette))
                    
                    for i, color in enumerate(palette):
                        # Convert RGB (e.g., 255, 255, 255) to a Hex String (e.g., #FFFFFF)
                        hex_code = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2]).upper()
                        
                        with cols[i]:
                            # Draw the colored square (removed the HTML text so it doesn't duplicate)
                            st.markdown(f'''
                                <div style="background-color: {hex_code}; height: 60px; border-radius: 8px; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 8px;"></div>
                            ''', unsafe_allow_html=True)
                            
                            # Use Streamlit's native code block for the automatic copy button
                            st.code(hex_code, language="plaintext")
                            
                except Exception as e:
                    st.error(f"Could not extract colors: {e}")
