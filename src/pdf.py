import img2pdf


def convert_image_to_pdf(image_path, pdf_path):
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(image_path))

    return pdf_path