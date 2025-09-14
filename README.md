📚 AI Study Bot (Flask + LangChain + Gemini RAG)

An AI-powered Study Assistant built with Flask, LangChain, FAISS, HuggingFace embeddings, and Google Gemini API.
This app allows you to upload PDFs or text files, automatically build a knowledge index, and ask natural language questions with structured, well-formatted answers.

✨ Features

📂 Upload PDFs or text files as knowledge base

🔍 FAISS vector search for fast document retrieval

🧠 HuggingFace embeddings (all-MiniLM-L6-v2) for semantic search

🤖 Google Gemini API for structured answers (Markdown headings, bullet points, examples)

🎨 Flask web UI with endpoints for file upload and Q&A

📝 Answers are well-structured:

Definition

Key Concepts

Detailed Explanation

Example

Summary

⚙️ Tech Stack

Python 3.10+

Flask

LangChain

FAISS

HuggingFace Sentence Transformers

Google Gemini

🛠️ Installation & Setup
1. Clone Repository
git clone https://github.com/your-username/ai-study-bot.git
cd ai-study-bot

2. Create Virtual Environment
python -m venv AiStudyBot
# Activate (Windows)
AiStudyBot\Scripts\activate
# Activate (Linux/Mac)
source AiStudyBot/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Setup Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_google_gemini_api_key

▶️ Running the App

Start Flask server:

python app.py


App runs at:
👉 http://127.0.0.1:8000

📡 API Endpoints
1. Home
GET /


Loads the frontend (index.html).

2. Upload Files
POST /upload


Upload PDFs or text files for indexing.

Example (cURL):

curl -X POST -F "files=@notes.pdf" http://127.0.0.1:8000/upload


Response:

{
  "status": "index built",
  "docs": 12
}

3. Ask a Question
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

When you ask:

{"question": "Explain SSDLC"}


Answer will be structured:

## Definition
Secure Software Development Life Cycle (SSDLC) is ...

## Key Concepts
● **Proactive Security** – Security integrated early  
● **Reduced Vulnerabilities** – Less risk in final product  
● **Cost Savings** – Fix issues early  

## Detailed Explanation
...

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

🔄 Add authentication (optional)

🔄 Improve UI with Bootstrap/Tailwind

🔄 Export answers as PDF/Markdown

🤝 Contributing

Pull requests are welcome! If you’d like to contribute, please fork the repo and create a feature branch.
