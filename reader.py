import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
import os

# Set page configuration
st.set_page_config(page_title="📖 Hari's File Reader", layout="wide")

# Title and instructions
st.title("📚 Hari Prakash's File Reader")
st.markdown("Upload and view **text**, **PDF**, or **image** files in-browser.")

# Set upload directory
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File uploader
uploaded_files = st.file_uploader(
    "📤 Upload your files (.txt, .pdf, .png, .jpg)",
    type=["txt", "pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Save uploaded files
if uploaded_files:
    for file in uploaded_files:
        save_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
    st.success("✅ Files uploaded successfully!")

# Sidebar file browser
st.sidebar.header("📂 Your Library")
file_list = os.listdir(UPLOAD_FOLDER)

# If there are files, show them in the sidebar
if file_list:
    selected_file = st.sidebar.selectbox("Choose a file to read/view", file_list)

    if selected_file:  # Make sure a file is actually selected
        file_path = os.path.join(UPLOAD_FOLDER, selected_file)
        file_ext = selected_file.lower().split('.')[-1]

        st.subheader(f"🗂️ Now Viewing: {selected_file}")

        # Display based on file type
        if file_ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.text_area("📖 Text File Content", content, height=400)

        elif file_ext == "pdf":
            reader = PdfReader(file_path)
            all_text = "\n\n".join([page.extract_text() or "" for page in reader.pages])
            st.text_area("📄 PDF File Content", all_text, height=500)

        elif file_ext in ["png", "jpg", "jpeg"]:
            image = Image.open(file_path)
            st.image(image, caption=selected_file, use_column_width=True)

        else:
            st.warning("⚠️ Unsupported file format.")
else:
    st.sidebar.info("No files uploaded yet. Upload to begin reading.")
