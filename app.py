from src.scanner import scan_document
from src.pdf import convert_image_to_pdf


def main():
    input_path = "input-images/sample.jpg"
    scanned_image_path = "output-scans/scanned-output.jpg"
    pdf_path = "output-scans/scanned-document.pdf"

    try:
        scan_document(input_path, scanned_image_path)
        convert_image_to_pdf(scanned_image_path, pdf_path)

        print("Document scanned successfully!")
        print("Image saved at:", scanned_image_path)
        print("PDF saved at:", pdf_path)

    except Exception as error:
        print("Something went wrong.")
        print("Error:", error)


if __name__ == "__main__":
    main()