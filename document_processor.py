from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        raw_text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                raw_text += extracted + "\n"

        return raw_text.strip()
    except Exception as e:
        return str(e)
