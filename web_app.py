import os
import streamlit as st
from PIL import Image

from src.scanner import scan_document
from src.pdf import convert_image_to_pdf
from src.qr import detect_qr_code
from src.analyzer import analyze_document


st.set_page_config(
    page_title="Smart Document Scanner",
    layout="wide"
)

st.title("Smart Document Scanner & Analyzer")
st.write("Upload a document image, scan it, export it, detect QR codes, and analyze resume text.")

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

            qr_result = detect_qr_code(input_path)

            if qr_result:
                st.subheader("QR Code Result")
                st.write(qr_result)

                if qr_result.startswith("http://") or qr_result.startswith("https://"):
                    st.link_button("Open QR Link", qr_result)
            else:
                st.info("No QR code detected in this image.")

            st.success("Document scanned successfully!")

        except Exception as error:
            st.error("Something went wrong.")
            st.error(error)


st.divider()

st.subheader("Resume / Document Analyzer")
st.write("Paste resume or document text below to extract useful information.")

document_text = st.text_area(
    "Paste text here",
    height=220
)

if st.button("Analyze Text"):
    if document_text.strip() == "":
        st.warning("Please paste some text first.")
    else:
        analysis = analyze_document(document_text)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Document Type", analysis["document_type"])

        with col2:
            st.metric("Emails Found", len(analysis["emails"]))

        with col3:
            st.metric("Skills Found", len(analysis["skills"]))

        st.subheader("Extracted Details")

        st.write("Emails:", analysis["emails"] if analysis["emails"] else "No email found")
        st.write("Phone Numbers:", analysis["phones"] if analysis["phones"] else "No phone number found")
        st.write("Skills:", analysis["skills"] if analysis["skills"] else "No skills found")

        if analysis["document_type"] == "Resume":
            st.subheader("Resume Score")
            st.progress(analysis["score"] / 100)
            st.write(f"Score: {analysis['score']} / 100")

            st.subheader("Suggestions")
            for suggestion in analysis["suggestions"]:
                st.write("-", suggestion)