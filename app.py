import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# LangChain
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_community.vectorstores import FAISS

# Gemini
import google.generativeai as genai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ------------------------
# Config
# ------------------------
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)
INDEX_PATH = Path("faiss_index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4

app = Flask(__name__)

_vectorstore = None

# ✅ Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Set GEMINI_API_KEY environment variable")
genai.configure(api_key=GEMINI_API_KEY)

# ------------------------
# Helpers
# ------------------------
def save_files(files):
    paths = []
    for file in files:
        filename = secure_filename(file.filename)
        path = UPLOAD_DIR / filename
        file.save(path)
        paths.append(path)
    return paths

def load_documents(paths):
    docs = []
    for path in paths:
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            docs.extend(loader.load())
        else:
            loader = TextLoader(str(path), encoding="utf-8")
            docs.extend(loader.load())
    return docs

def build_index(docs):
    global _vectorstore
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    split_docs = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    _vectorstore = FAISS.from_documents(split_docs, embeddings)
    _vectorstore.save_local(str(INDEX_PATH))

def load_index():
    global _vectorstore
    if _vectorstore is None and INDEX_PATH.exists():
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        _vectorstore = FAISS.load_local(
            str(INDEX_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )
    return _vectorstore

def retrieve(query, k=TOP_K):
    vs = load_index()
    if not vs:
        return []
    retriever = vs.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)

def build_prompt(question, docs):
    context = ""
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source", f"doc_{i}")
        snippet = d.page_content[:500].replace("\n", " ")
        context += f"[{src}] {snippet}\n\n"
    return f"""
You are a helpful tutor. Use the provided CONTEXT to answer the QUESTION.  
⚡ Formatting Rules (must follow strictly):  
1. Always use **Markdown headings** (`##`, `###`).  
2. Each section must be **separated by a line break**.  
3. Use **bullet points (●)** for lists.  
4. Keep sentences short and simple (max 2–3 lines per point).  
5. Avoid writing multiple sections in a single paragraph.  

⚡ Very Important Instructions:
- Always follow this structure in your answer:

## Definition
- A short, clear definition of the main concept.

## Key Concepts
- Use bullet points (●) with **bold keywords**.  
- Keep each point short and easy to understand.

## Detailed Explanation
- Break down the topic into logical sub-sections.  
- Use **subheadings** if needed.  
- Write in simple, concise language (3–4 lines per paragraph).  
- Avoid long walls of text.

## Example
- Provide a **practical example** (real-world, analogy, or mini code snippet).  
- Make sure it connects to the QUESTION.  

## Summary
- End with **3–5 bullet points** highlighting the most important takeaways.

---

CONTEXT:  
{context}  

QUESTION:  
{question}  

ANSWER:

"""

def ask_gemini(prompt, model="gemini-1.5-flash", max_output_tokens=512):
    model = genai.GenerativeModel(model)
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": max_output_tokens}
    )
    return response.text

# ------------------------
# Routes
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    paths = save_files(request.files.getlist("files"))
    docs = load_documents(paths)
    build_index(docs)
    return jsonify({"status": "index built", "docs": len(docs)})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"error": "Send JSON like {'question': 'your question'}"}), 400
    question = data["question"]
    docs = retrieve(question, TOP_K)
    if not docs:
        return jsonify({"error": "No documents indexed"}), 400
    prompt = build_prompt(question, docs)
    answer = ask_gemini(prompt)
    sources = [
        {"source": d.metadata.get("source", "unknown"),
         "snippet": d.page_content[:200]}
        for d in docs
    ]
    return jsonify({"answer": answer, "sources": sources})

# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    app.run(port=8000, debug=True)
