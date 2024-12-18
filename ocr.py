import os
import subprocess
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader, PdfWriter

def pdf_to_images(pdf_path, output_dir):
    """
    Converte o PDF em imagens PNG usando o pdftoppm.
    """
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(['pdftoppm', pdf_path, os.path.join(output_dir, 'page'), '-png'], check=True)

def image_to_pdf(image_path):
    """
    Converte uma imagem para PDF usando OCR.
    """
    return pytesseract.image_to_pdf_or_hocr(Image.open(image_path), extension='pdf')

def merge_pdfs(output_path, pdf_pages):
    """
    Mescla páginas de PDFs em um único arquivo.
    """
    pdf_writer = PdfWriter()
    for pdf_page in pdf_pages:
        pdf_reader = PdfReader(pdf_page)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    with open(output_path, "wb") as out_file:
        pdf_writer.write(out_file)

def process_pdf(pdf_path):
    """
    Processa o PDF, realiza OCR, e substitui o original pelo processado.
    """
    temp_dir = os.path.join(os.path.dirname(pdf_path), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Passo 1: Converter PDF para imagens
        pdf_to_images(pdf_path, temp_dir)

        # Passo 2: Realizar OCR em imagens e criar PDFs
        temp_pdfs = []
        for image_file in sorted(os.listdir(temp_dir)):
            if image_file.endswith(".png"):
                image_path = os.path.join(temp_dir, image_file)
                pdf_content = image_to_pdf(image_path)
                temp_pdf_path = os.path.join(temp_dir, f"{os.path.splitext(image_file)[0]}.pdf")
                with open(temp_pdf_path, "wb") as pdf_file:
                    pdf_file.write(pdf_content)
                temp_pdfs.append(temp_pdf_path)

        # Passo 3: Mesclar PDFs temporários em um único arquivo
        final_pdf_path = os.path.join(temp_dir, "final_output.pdf")
        merge_pdfs(final_pdf_path, temp_pdfs)

        # Passo 4: Substituir o arquivo original pelo processado
        os.replace(final_pdf_path, pdf_path)

        print(f"Processo concluído. Arquivo processado salvo em: {pdf_path}")
    finally:
        # Limpeza do diretório temporário
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python process_pdf.py <caminho_do_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    process_pdf(pdf_path)
