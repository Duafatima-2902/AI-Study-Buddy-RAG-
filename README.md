📚 AI Study Bot (Flask + LangChain + Gemini RAG)

An AI-powered Study Assistant built with Flask, LangChain, FAISS, HuggingFace embeddings, and Google Gemini API.

Upload PDFs or text files 📂, automatically build a knowledge index 🗂️, and ask natural language questions 🤖 with structured, well-formatted answers.

✨ Features

📂 Upload PDFs or text files as a knowledge base

🔍 FAISS vector search for lightning-fast document retrieval

🧠 HuggingFace embeddings (all-MiniLM-L6-v2) for semantic similarity

🤖 Google Gemini API for structured AI answers (Markdown headings, bullets, examples)

🎨 Flask web UI with REST endpoints

📝 Structured Answers always include:

✅ Definition

✅ Key Concepts

✅ Detailed Explanation

✅ Example

✅ Summary

⚙️ Tech Stack

🐍 Python 3.10+

🌐 Flask

🔗 LangChain

📊 FAISS

🤗 HuggingFace Sentence Transformers

🌟 Google Gemini API

🛠️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/Duafatima-2902/AI-Study-Buddy-RAG-.git
cd ai-study-bot

2️⃣ Create Virtual Environment
python -m venv AiStudyBot


Activate it:

Windows

AiStudyBot\Scripts\activate


Linux/Mac

source AiStudyBot/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_google_gemini_api_key

▶️ Running the App

Start Flask server:

python app.py


App will run at:
👉 http://127.0.0.1:8000

📡 API Endpoints
🏠 Home
GET /


Loads the frontend (index.html).

📂 Upload Files
POST /upload


Upload PDFs or text files for indexing.

Example:

curl -X POST -F "files=@notes.pdf" http://127.0.0.1:8000/upload


Response:

{
  "status": "index built",
  "docs": 12
}

❓ Ask a Question
POST /ask


Query the knowledge base.

Example:

curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain SSDLC"}'


Response:

{
  "answer": "## Definition\nSSDLC is ...",
  "sources": [
    {"source": "uploaded_files/notes.pdf", "snippet": "SSDLC integrates security..."}
  ]
}

🧪 Example Output

Input:

{"question": "Explain Phases of penetration testing"}


Answer:
<img width="1917" height="862" alt="image" src="https://github.com/user-attachments/assets/28acf2e5-9ef6-458d-b765-e5aa0d34bfab" />

## Definition
Phases of penetration testing are ...

## Key Concepts
● **Proactive Security** – Integrated early  
● **Reduced Vulnerabilities** – Lower risks in final product  
● **Cost Savings** – Fix issues early  

## Detailed Explanation
... (structured breakdown)

## Example
Imagine a mobile banking app...

## Summary
● Secure development  
● Lower costs  
● Better compliance

📂 Project Structure
ai-study-bot/
│── app.py                # Flask backend
│── templates/
│    └── index.html       # Frontend UI
│── uploaded_files/       # Uploaded documents
│── faiss_index/          # FAISS vector DB
│── requirements.txt      # Dependencies
│── .env                  # API key (ignored in git)

🚀 Roadmap

✅ Basic Q&A from PDFs

✅ Structured answers (headings + bullets)

🔄 Add authentication (JWT/Session-based)

🔄 Improve UI with Bootstrap/Tailwind

🔄 Export answers as PDF/Markdown

🤝 Contributing

Pull requests are welcome!
If you’d like to contribute:

Fork the repo

Create a feature branch

Commit changes

Open a PR 🎉
