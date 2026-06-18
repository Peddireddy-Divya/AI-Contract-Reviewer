from flask import Flask, render_template, request
import pdfplumber
import os
import ollama

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def generate_summary(text):

    prompt = f"""
    Analyze this document and provide:

    1. Summary
    2. Key Information
    3. Important Points

    Document:

    {text[:4000]}
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["pdf"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    contract_text = extract_text(filepath)

    summary = "AI Summary Working Successfully"

    return render_template(
        "result.html",
        contract_text=contract_text,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)