# MonkCloud - A Inhouse Cloud Storage

## Introduction
MonkCloud is an in-house cloud solution built using **Flask** (Python) and **HTML/CSS** for private file storage and management. This project allows users to **upload, download, and manage files** securely within a private infrastructure. Compared to public cloud solutions, an in-house cloud offers better control over resources and security.

## Objectives
The primary goal of MonkCloud is to provide a **lightweight, user-friendly** cloud storage solution with the following features:
- **File Upload & Download**: Users can upload and retrieve files through a web-based interface.
- **Basic File Management**: A simple dashboard for managing stored files.
- **Flask Backend**: Handles HTTP requests for file handling and UI rendering.
- **HTML/CSS Frontend**: Provides an interactive and responsive user interface.
- **Authentication (Optional)**: Basic login system to restrict access.

## Technologies Used
- **Flask (Python)**: Micro-framework for handling requests and rendering web pages.
- **HTML/CSS**: For structuring and designing the user interface.
- **SQLite (Optional)**: For storing file metadata and user details.
- **JavaScript (Optional)**: Enhances UI interactions such as real-time file listing.

## System Architecture
MonkCloud is structured into the following components:
- **Frontend (HTML/CSS/JavaScript)**: Web-based user interface for file operations.
- **Backend (Flask)**: Manages API requests and serves web pages.
- **Database (Optional - SQLite)**: Stores file metadata and user information.
- **File Storage**: Maintains uploaded files in a server directory.

## Key Features
✅ **File Upload**: Users can upload files to the server.  
✅ **File Download**: Retrieve uploaded files securely.  
✅ **File Management**: View, delete, and organize stored files.  
✅ **User Authentication (Optional)**: Restrict access to authorized users.  
✅ **Responsive UI**: Designed to work on various devices.

## Advantages of Flask
🚀 **Lightweight & Flexible**: Flask is a micro-framework that offers full control over customizations.  
📚 **Easy to Learn**: Ideal for beginners and rapid prototyping.  
🔌 **Extensibility**: Supports various plugins like authentication, database integration, and more.  
🌎 **Strong Community Support**: Extensive documentation and active developer community.

## Installation & Setup
### 1. Clone the Repository
```bash
git clone https://github.com/DivyamOswal/MonkCloud.git
cd MonkCloud
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Flask Application
```bash
python app.py
```

### 4. Access MonkCloud
Visit `http://127.0.0.1:5000/` in your browser.

## Future Enhancements
- ✅ Implement user authentication for secure access.
- ✅ Add database support for file metadata storage.
- ✅ Improve UI with JavaScript-based file operations.
- ✅ Enable cloud synchronization with external storage solutions.

## License
This project is licensed under the **MIT License**.

---
🔗 **GitHub Repository**: [MonkCloud](https://github.com/DivyamOswal/MonkCloud)  
📧 **Contact**: divyamoswal@example.com

