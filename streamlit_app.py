import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
import zipfile


def convert_pdf_to_images(pdf_file):
    """Convert PDF to a list of JPEG images."""
    images = convert_from_bytes(pdf_file.read())
    return images


def convert_images_to_pdf(image_file):
    """Convert a single JPEG image to a PDF."""
    image = Image.open(image_file).convert("RGB")
    pdf_bytes = io.BytesIO()
    image.save(pdf_bytes, format="PDF")
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


st.title("PDF-JPG Converter")

uploaded_file = st.file_uploader("Upload a PDF or JPEG file", type=["pdf", "jpg", "jpeg"])

if uploaded_file:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
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

    elif file_type in ["image/jpeg", "image/jpg"]:
        st.info("Processing JPEG file...")
        pdf_file = convert_images_to_pdf(uploaded_file)
        st.success("JPEG image converted to PDF successfully!")
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="converted_file.pdf",
            mime="application/pdf"
        )

    else:
        st.error("Unsupported file type. Please upload a valid PDF or JPEG file.")
