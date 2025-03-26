import socket
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from fpdf import FPDF
from pdfminer.high_level import extract_text
from PIL import Image

HOST = "127.0.0.1"
PORT = 12345
server_running = False
server_socket = None

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

def handle_client(client_socket, addr, log_area):
    try:
        log_area.insert(tk.END, f"🔗 Connection from {addr}\n")

        conversion_type = client_socket.recv(1024).decode().strip()
        log_area.insert(tk.END, f"📥 Conversion request: {conversion_type}\n")

        filename = client_socket.recv(1024).decode().strip()
        log_area.insert(tk.END, f"📂 Received filename: {filename}\n")

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
            return

        log_area.insert(tk.END, f"🔎 Checking for file: {input_filename}\n")

        if not os.path.exists(input_filename):
            log_area.insert(tk.END, f"❌ ERROR: {input_filename} not found!\n")
            client_socket.sendall(b"ERROR: File not found")
            client_socket.close()
            return

        if conversion_type == "TXT_TO_PDF":
            convert_txt_to_pdf(input_filename, output_filename)
        elif conversion_type == "PDF_TO_TXT":
            convert_pdf_to_txt(input_filename, output_filename)
        elif conversion_type in ["JPG_TO_PNG", "PNG_TO_JPG"]:
            convert_image(input_filename, output_filename)

        log_area.insert(tk.END, f"✅ Conversion successful: {output_filename}\n")
        success_message = f"Conversion successful: {output_filename}"
        client_socket.sendall(success_message.encode())
    except Exception as e:
        error_message = f"ERROR: {str(e)}"
        log_area.insert(tk.END, f"❌ {error_message}\n")
        client_socket.sendall(error_message.encode())
    finally:
        client_socket.close()

def start_server(log_area):
    global server_running, server_socket
    if server_running:
        messagebox.showwarning("Warning", "Server is already running!")
        return

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        server_running = True
        log_area.insert(tk.END, f"✅ Server started on {HOST}:{PORT}\n")

        while server_running:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, log_area))
            client_thread.start()

    except Exception as e:
        log_area.insert(tk.END, f"❌ Error: {str(e)}\n")
        stop_server(log_area)

def stop_server(log_area):
    global server_running, server_socket
    if not server_running:
        messagebox.showwarning("Warning", "Server is not running!")
        return

    server_running = False
    if server_socket:
        server_socket.close()
    log_area.insert(tk.END, "🛑 Server stopped.\n")

def start_server_thread(log_area):
    server_thread = threading.Thread(target=start_server, args=(log_area,))
    server_thread.daemon = True
    server_thread.start()

root = tk.Tk()
root.title("📡 File Conversion Server")
root.geometry("500x400")
root.configure(bg="#F0F4F8")

title_label = tk.Label(root, text="📡 File Conversion Server", font=("Arial", 16, "bold"), bg="#F0F4F8")
title_label.pack(pady=10)

log_area = scrolledtext.ScrolledText(root, width=60, height=15, font=("Arial", 10))
log_area.pack(pady=10)
log_area.insert(tk.END, "📝 Logs will appear here...\n")

button_frame = tk.Frame(root, bg="#F0F4F8")
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Server", command=lambda: start_server_thread(log_area), bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Stop Server", command=lambda: stop_server(log_area), bg="#F44336", fg="white", font=("Arial", 12, "bold"))
stop_button.grid(row=0, column=1, padx=10)

root.mainloop()
