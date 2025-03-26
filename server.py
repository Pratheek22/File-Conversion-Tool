import socket
import os
from fpdf import FPDF
from pdfminer.high_level import extract_text
from PIL import Image

HOST = "127.0.0.1"
PORT = 12345

def convert_txt_to_pdf(input_filename, output_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    with open(input_filename, "r", encoding="utf-8") as file:
        content = file.read()
    pdf.multi_cell(0, 10, content)
    pdf.output(output_filename)

def convert_pdf_to_txt(input_filename, output_filename):
    text = extract_text(input_filename)
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(text)

def convert_image(input_filename, output_filename):
    img = Image.open(input_filename)
    img = img.convert("RGB")
    img.save(output_filename)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    try:
        conversion_type = client_socket.recv(1024).decode().strip()
        print(f"[SERVER] Received conversion type: {conversion_type}")

        filename = client_socket.recv(1024).decode().strip()
        print(f"[SERVER] Received filename: {filename}")

        if conversion_type == "TXT_TO_PDF":
            input_filename = f"{filename}.txt"
            output_filename = f"converted_{filename}.pdf"
        elif conversion_type == "PDF_TO_TXT":
            input_filename = f"{filename}.pdf"
            output_filename = f"converted_{filename}.txt"
        elif conversion_type == "JPG_TO_PNG":
            input_filename = f"{filename}.jpg"
            output_filename = f"converted_{filename}.png"
        elif conversion_type == "PNG_TO_JPG":
            input_filename = f"{filename}.png"
            output_filename = f"converted_{filename}.jpg"
        else:
            client_socket.sendall(b"ERROR: Invalid conversion type")
            client_socket.close()
            continue

        print(f"[SERVER] Checking for file: {input_filename}")

        if not os.path.exists(input_filename):
            print(f"[SERVER] ERROR: {input_filename} not found!")
            client_socket.sendall(b"ERROR: File not found")
            client_socket.close()
            continue

        if conversion_type == "TXT_TO_PDF":
            convert_txt_to_pdf(input_filename, output_filename)
        elif conversion_type == "PDF_TO_TXT":
            convert_pdf_to_txt(input_filename, output_filename)
        elif conversion_type in ["JPG_TO_PNG", "PNG_TO_JPG"]:
            convert_image(input_filename, output_filename)

        print(f"[SERVER] File converted successfully: {output_filename}")
        success_message = f"Conversion successful: {output_filename}"
        client_socket.sendall(success_message.encode())

    except Exception as e:
        client_socket.sendall(f"ERROR: {str(e)}".encode())

    finally:
        client_socket.close()