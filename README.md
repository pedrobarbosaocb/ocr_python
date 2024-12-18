# PDF OCR Processor

Este script permite realizar OCR (reconhecimento óptico de caracteres) em documentos PDF, transformando imagens contidas no PDF em texto pesquisável e mantendo o formato original do documento.

## Funcionalidades

- Converte arquivos PDF em imagens utilizando `pdftoppm`.
- Realiza OCR em cada página do PDF utilizando a biblioteca `pytesseract`.
- Reconstrói o PDF com texto pesquisável.
- Substitui o PDF original pelo processado.

## Requisitos

Antes de usar o script, certifique-se de que todos os requisitos estão instalados:

### Softwares necessários
1. **pdftoppm** (parte do pacote Poppler)
   - Instale em sistemas baseados em Linux: `sudo apt install poppler-utils`
   - Em sistemas macOS, instale via Homebrew: `brew install poppler`
2. **Tesseract OCR**
   - Instale em sistemas baseados em Linux: `sudo apt install tesseract-ocr`
   - Em sistemas macOS, instale via Homebrew: `brew install tesseract`

### Bibliotecas Python
- Instale as dependências com o pip:
  ```bash
  pip install pytesseract PyPDF2 pillow
```

```shell
    python process_pdf.py documento.pdf
```