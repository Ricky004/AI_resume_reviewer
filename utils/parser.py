import pdfplumber

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            p_text = page.extract_text()
            if p_text:
                text += p_text + "\n"
        return text.strip()