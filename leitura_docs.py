import fitz  # PyMuPDF

def read_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

pdf_text = read_pdf('docs/livreto_contos.pdf')