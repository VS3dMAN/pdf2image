import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
import zipfile

def convert_pdf_to_images(pdf_file):
    """Convert PDF to a list of JPEG images."""
    images = convert_from_bytes(pdf_file.read())
    return images

def convert_images_to_pdf(image_files):
    """Convert multiple JPEG images to a single PDF."""
    images = [Image.open(image_file).convert("RGB") for image_file in image_files]
    pdf_bytes = io.BytesIO()
    images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
    pdf_bytes.seek(0)
    return pdf_bytes

def create_zip(images):
    """Create a zip file from a list of images."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for i, img in enumerate(images):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            zf.writestr(f"page_{i + 1}.jpg", img_byte_arr.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit App Interface
st.title("PDF-JPG Converter")

st.sidebar.header("Choose an Action")
action = st.sidebar.radio("Convert:", ["PDF to JPEG", "JPEG to PDF"])

if action == "PDF to JPEG":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file:
        st.info("Processing PDF file...")
        images = convert_pdf_to_images(uploaded_file)
        zip_file = create_zip(images)
        st.success("PDF converted to JPEG images successfully!")
        st.download_button(
            label="Download all images as ZIP",
            data=zip_file,
            file_name="converted_images.zip",
            mime="application/zip"
        )

elif action == "JPEG to PDF":
    uploaded_files = st.file_uploader(
        "Upload JPEG files", 
        type=["jpg", "jpeg"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.info("Processing JPEG files...")
        pdf_file = convert_images_to_pdf(uploaded_files)
        st.success("JPEG images converted to a single PDF successfully!")
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="converted_file.pdf",
            mime="application/pdf"
        )
