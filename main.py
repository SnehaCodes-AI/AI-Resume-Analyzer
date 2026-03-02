from flask import Flask, render_template, request
from analyse_pdf import analyze_resume_gemini
import pymupdf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    score = 0
    if request.method == "POST":
        jd = request.form.get("job_description")
        file = request.files.get("resume")
        
        if file and jd:
            doc = pymupdf.open(stream=file.read(), filetype="pdf")
            resume_text = "".join([page.get_text() for page in doc])
            
            # Receive both the clean text and the integer score
            report, score = analyze_resume_gemini(resume_text, jd)
            
    return render_template("index.html", report=report, score=score)

if __name__ == "__main__":
    app.run(debug=True)