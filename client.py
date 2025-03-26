import tkinter as tk
from tkinter import messagebox, ttk
import socket
import time

HOST = "127.0.0.1"
PORT = 12345

def send_conversion_request():
    conversion_options = {
        "TXT to PDF": "TXT_TO_PDF",
        "PDF to TXT": "PDF_TO_TXT",
        "JPG to PNG": "JPG_TO_PNG",
        "PNG to JPG": "PNG_TO_JPG"
    }

    conversion_type = conversion_var.get()
    filename = filename_entry.get().strip()

    if not filename:
        messagebox.showerror("Error", "Please enter a valid filename.")
        return

    if conversion_type not in conversion_options:
        messagebox.showerror("Error", "Please select a valid conversion type.")
        return

    try:
        status_label.config(text="⏳ Connecting to server...")
        root.update()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.sendall(conversion_options[conversion_type].encode())
        time.sleep(0.1)
        client_socket.sendall(filename.encode())
        time.sleep(0.1)
        response = client_socket.recv(1024).decode()
        client_socket.close()

        if "successful" in response:
            messagebox.showinfo("Success", response)
            status_label.config(text="✅ Conversion Successful!")
        else:
            messagebox.showerror("Error", response)
            status_label.config(text="❌ Conversion Failed!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server:\n{str(e)}")
        status_label.config(text="❌ Connection Error!")

root = tk.Tk()
root.title("✨ File Conversion Tool ✨")
root.geometry("450x350")
root.config(bg="#F0F4F8")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), background="#4CAF50", foreground="white")
style.configure("TLabel", font=("Arial", 12), background="#F0F4F8", foreground="#333333")
style.configure("TCombobox", font=("Arial", 12))

title_label = tk.Label(root, text="🔄 File Conversion Tool", font=("Arial", 18, "bold"), bg="#F0F4F8", fg="#333333")
title_label.pack(pady=15)

conversion_var = tk.StringVar()
conversion_var.set("Select Conversion Type")

conversion_options = ["TXT to PDF", "PDF to TXT", "JPG to PNG", "PNG to JPG"]
conversion_menu = ttk.Combobox(root, textvariable=conversion_var, values=conversion_options, width=35, state="readonly")
conversion_menu.pack(pady=10)

filename_label = tk.Label(root, text="📂 Enter filename (without extension):", font=("Arial", 12), bg="#F0F4F8", fg="#333333")
filename_label.pack(pady=5)

filename_entry = tk.Entry(root, width=40, font=("Arial", 12), bd=2, relief="solid")
filename_entry.pack(pady=5)

convert_button = tk.Button(root, text="⚡ Convert File", command=send_conversion_request, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5, bd=0, relief="ridge", cursor="hand2")
convert_button.pack(pady=20)

status_label = tk.Label(root, text="", font=("Arial", 12), bg="#F0F4F8", fg="#333333")
status_label.pack()

footer_label = tk.Label(root, text="Created with ❤️ using Python", font=("Arial", 10), bg="#F0F4F8", fg="#888888")
footer_label.pack(pady=10)

root.mainloop()
