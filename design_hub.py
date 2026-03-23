import streamlit as st

# Set up the page
st.set_page_config(page_title="Design Organizer", page_icon="🎨", layout="centered")

st.title("🎨 Design Asset & Prompt Organizer")
st.markdown("A centralized hub for graphic assets, colors, and generator prompts.")

# Create tabs for different asset types
tab1, tab2, tab3 = st.tabs(["🎨 Brand Colors", "📝 Prompt Library", "🖼️ Layout References"])

# --- TAB 1: Brand Colors ---
with tab1:
    st.header("Color Palette")
    st.write("Save your most used hex codes here.")
    
    col1, col2 = st.columns(2)
    with col1:
        color1 = st.color_picker("Primary Color", "#1E88E5")
        st.code(color1, language="plaintext") # Makes the hex code easy to copy
    with col2:
        color2 = st.color_picker("Accent Color", "#D81B60")
        st.code(color2, language="plaintext")

# --- TAB 2: Prompt Library ---
with tab2:
    st.header("Generator Prompts")
    st.write("Store your best text prompts for generating backgrounds and elements.")
    
    # Example of a saved prompt
    st.subheader("Saved Prompt: Corporate Background")
    st.code("Abstract geometric background, professional blue and silver tones, clean lines, 8k resolution", language="plaintext")
    
    st.divider()
    
    # Input for new prompts (UI only for now)
    new_prompt = st.text_area("Draft a new prompt:")
    if st.button("Save Prompt"):
        st.success("Prompt drafted! (Database connection needed to save permanently)")

# --- TAB 3: Reference Gallery ---
with tab3:
    st.header("Reference Uploads")
    st.write("Upload layouts or inspiration images.")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Reference", use_container_width=True)
