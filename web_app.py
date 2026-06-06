import os
import streamlit as st
from PIL import Image

from src.scanner import scan_document
from src.pdf import convert_image_to_pdf


st.set_page_config(
    page_title="Smart Document Scanner",
    page_icon="📄",
    layout="wide"
)


st.title("Smart Document Scanner")
st.write("Upload a document image, scan it, and export it as an image or PDF.")


uploaded_file = st.file_uploader(
    "Upload document image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:
    input_path = os.path.join("input-images", uploaded_file.name)
    scanned_image_path = os.path.join("output-scans", "scanned-output.jpg")
    pdf_path = os.path.join("output-scans", "scanned-document.pdf")

    with open(input_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("Original Image")
        original_image = Image.open(input_path)
        st.image(original_image, use_container_width=True)

    if st.button("Scan Document"):
        try:
            scan_document(input_path, scanned_image_path)
            convert_image_to_pdf(scanned_image_path, pdf_path)

            with right_column:
                st.subheader("Scanned Result")
                scanned_image = Image.open(scanned_image_path)
                st.image(scanned_image, use_container_width=True)

                with open(scanned_image_path, "rb") as image_file:
                    st.download_button(
                        label="Download Scanned Image",
                        data=image_file,
                        file_name="scanned-output.jpg",
                        mime="image/jpeg"
                    )

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name="scanned-document.pdf",
                        mime="application/pdf"
                    )

            st.success("Document scanned successfully!")

        except Exception as error:
            st.error("Something went wrong.")
            st.error(error)