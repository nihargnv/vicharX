
# **📄 VicharX - Intelligent Document Management System**  

A **Django-based** web application for managing, searching, and analyzing documents with AI-powered features. The platform supports **semantic search, metadata extraction, analytics, and cloud storage integration**.



## **🚀 Features**
- 📂 **Upload & Manage Documents**
- 🔍 **Smart Search** (Full-text, Keyword, Semantic)
- 📊 **Analytics Dashboard**
- 🗑️ **Delete & Organize Files**
- 🌐 **Deployed on Google Cloud Platform (GCP)**
**- **for more details please view the intro video  -  https://youtu.be/KVLKekJYSkM ****

## **📁 Folder Structure**
```
/your-project
│── docsapp/         # Django app (Views, Models, Templates)
│── static/          # CSS, JS, Images
│── templates/       # HTML templates
│── requirements.txt # Dependencies
│── manage.py        # Django Entry Point
│── app.yaml         # GCP Deployment Config
│── README.md        # Documentation
```

## **📦 Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/your-project.git
cd your-project
```
## **🛠 Configuration**

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

*** Please make Sure that you have run the "initial_run.py" file before implementing the further steps. ***

### **4️⃣ Apply Migrations**
```sh
python manage.py migrate
```

### **5️⃣ Run the Server**
```sh
python manage.py runserver
```

Visit: **`http://127.0.0.1:8000/`** in your browser.


### **Technologies Used:**
1. HTML, CSS and JS for the Frontend.
2. Python Django for the Backend.
3. SQL DataBase for storing the files and the data.
4. Implemented OCR and Image Captioning(BLIP Transformer) to understand Image data.
5. Can handle most types of files. [png, pdf, jpg, jpeg, xlsx, docx, pptx, txt]
6. Implemented Text Summarization model (PreTrained and Optimised AI Model from Transformers, HuggingFace).
7. BART Classifier to classify the files based on the file content.
8. Implemented Semantic search on the files.
9. Deployed on GCP - http://34.35.9.73/



with Love
    - team Vision Forge...
