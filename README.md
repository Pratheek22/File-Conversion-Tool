# File-Conversion-Tool
# 📚 File Conversion Tool

This project is a **File Conversion Tool** built using Python and `tkinter` for the GUI. It connects to a server via **sockets** and supports multiple file format conversions. The tool provides a simple and interactive interface where users can choose the file conversion type and enter the filename to process.

---

## 🚀 Features
✅ Easy-to-use GUI with an attractive design  
✅ Supports the following file conversions:
- TXT to PDF  
- PDF to TXT  
- JPG to PNG  
- PNG to JPG  

✅ Server-client architecture using Python sockets  
✅ Error handling and informative message popups  

---

## 🖥️ Technologies Used
- Python
- Tkinter (for GUI)
- Socket Programming
- Time Library

---

## 📄 File Structure
📁 File converter 
├── 📄 client.py # Main client-side application with GUI 
├── 📄 server.py # Server-side script to handle file conversions 
├── 📄 requirements.txt # List of required packages 
└── 📄 README.md # Documentation

## 📝 Usage Instructions

1. Launch the `client.py` file.  
2. Select the desired file conversion type from the dropdown.  
3. Enter the filename without the extension (e.g., `sample` instead of `sample.txt`).  
4. Click on **Convert File** to initiate the conversion.  
5. The converted file will be saved in the output directory, and a success message will be displayed.  

---

## ⚡️ Error Handling
- Shows an error message if:
    - No valid file is selected.
    - Conversion type is not selected.
    - Connection to the server fails.
- Displays a success message if the conversion is successful.

---

## 🛠️ Troubleshooting
- If the server is not running, the client will be unable to establish a connection.
- Make sure the ports are correctly configured in both `client.py` and `server.py`.

---
![image](https://github.com/user-attachments/assets/7dde9a90-200e-4aae-b67b-264ec1ab5f3d)

![image](https://github.com/user-attachments/assets/8730247a-e1c9-4a85-b6a2-fe75d139e04a)

