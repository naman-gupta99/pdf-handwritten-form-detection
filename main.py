import fitz  # PyMuPDF
from PIL import Image
from image_matcher.image_matcher import get_image_matcher

IMAGE_MAPPER = get_image_matcher("ssim")

def pdf_page_to_image(pdf_path: str, page_number:int, dpi=200) -> Image:
    """
    Converts a specified page of a PDF to an image.

    Args:
        pdf_path (str): Path to the PDF file.
        page_number (int): Page number to convert (0-based index).
        dpi (int): Dots per inch for the output image.

    Returns:
        PIL.Image: Image of the specified PDF page.
    """
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)
    zoom = dpi / 72  # 72 is the default DPI for PDFs
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    mode = "RGB" if pix.alpha == 0 else "RGBA"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    return img

def find_matching_pages(reference_pdf:str, input_pdf:str) -> list[int]:
    """
    Finds pages in the input PDF that match the reference PDF.

    Args:
        reference_pdf (str): Path to the reference PDF (single-page).
        input_pdf (str): Path to the input PDF (multi-page).

    Returns:
        list: List of 1-based page numbers in input_pdf that match the reference.
    """
    reference_image = pdf_page_to_image(reference_pdf, 0)
    doc = fitz.open(input_pdf)
    matching_pages = []
    
    for page_num in range(len(doc)):
        input_image = pdf_page_to_image(input_pdf, page_num)
        if IMAGE_MAPPER.match(reference_image, input_image):
            matching_pages.append(page_num + 1)  # Page numbers are 1-based
            input_image.save(f"output/input_page_{page_num}.png")
    return matching_pages

if __name__ == "__main__":
    reference_pdf = 'input/reference.pdf'
    input_pdf = 'input/input.pdf'
    matching_pages = find_matching_pages(reference_pdf, input_pdf)
    print(f"Matching pages: {matching_pages}")
