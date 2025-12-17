from flask import Flask, render_template, request
import PyPDF2
import random
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET","POST"])
def index():
    questions=[]
    success=None

    if request.method=="POST":
        pdf=request.files.get("pdf")
        if not pdf or pdf.filename=="":
            return render_template("index.html", error="Please upload a PDF file")

        path=os.path.join(app.config["UPLOAD_FOLDER"], pdf.filename)
        pdf.save(path)
        success="PDF uploaded successfully"

        text=""
        with open(path,"rb") as f:
            reader=PyPDF2.PdfReader(f)
            for page in reader.pages:
                if page.extract_text():
                    text+=page.extract_text()

        sentences=[s.strip() for s in text.split(".") if len(s.strip())>30]

        used=set()
        while len(questions)<10 and len(sentences)>0:
            s=random.choice(sentences)
            if s in used: continue
            used.add(s)
            words=[w for w in s.split() if w.isalpha() and len(w)>4]
            if len(words)<4: continue
            answer=random.choice(words)
            options=random.sample(words,min(4,len(words)))
            if answer not in options:
                options[0]=answer
            random.shuffle(options)
            questions.append({
                "question":s.replace(answer,"_____"),
                "options":options,
                "answer":answer
            })

    return render_template("index.html", questions=questions, success=success)

if __name__=="__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
