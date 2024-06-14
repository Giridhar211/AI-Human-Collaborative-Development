from PyPDF2 import PdfReader
import openai
from fpdf import FPDF


def create_pdf(text_data, output_filename):
    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Add a cell
    pdf.multi_cell(200, 10, txt=text_data, border=0, align='L')

    # Save the pdf with name .pdf
    pdf.output(output_filename)


def filter_information(pdf, query):
    pdfreader = PdfReader(pdf)
    num_pages = len(pdfreader.pages)

    # read text from pdf
    raw_text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    # Set your OpenAI API key
    api_key = ''
    openai.api_key = api_key

    text = raw_text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
            {"role": "assistant", "content": query}
        ]
    )
    return response['choices'][0]['message']['content']


# Example query to filter information
# query_to_filter = "find how to connect to onvif camera & retrieve device information"
# "Filter out relevant details about the topic."

# Get filtered information
