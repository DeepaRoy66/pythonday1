from flask import Flask, render_template, request
import PyPDF2
import random
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------- HOME PAGE ----------
@app.route("/", methods=["GET", "POST"])
def index():
    questions = []

    if request.method == "POST":
        pdf = request.files["pdf"]

        if pdf.filename == "":
            return render_template("index.html", error="No file selected")

        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf.filename)
        pdf.save(pdf_path)

        # Read PDF
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 30]

        if len(sentences) < 5:
            return render_template("index.html", error="PDF content too small")

        # Generate MCQs
        used = set()
        while len(questions) < 10:
            s = random.choice(sentences)
            if s in used:
                continue
            used.add(s)

            words = s.split()
            keywords = [w for w in words if w.isalpha() and len(w) > 4]

            if len(keywords) < 4:
                continue

            answer = random.choice(keywords)
            question = s.replace(answer, "_____")

            options = random.sample(keywords, 3)
            if answer not in options:
                options.append(answer)
            random.shuffle(options)

            questions.append({
                "question": question,
                "options": options,
                "answer": answer
            })

    return render_template("index.html", questions=questions)

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    app.run(debug=True)
