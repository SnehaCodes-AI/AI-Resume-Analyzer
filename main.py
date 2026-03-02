import os
import io
import pymupdf  # Ensure 'pip install pymupdf' was run
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from analyse_pdf import analyze_resume_gemini
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_resume(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        doc.close()
        return text
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files.get("resume")
        jd = request.form.get("job_description")
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            
            text = extract_text_from_resume(path)
            result = analyze_resume_gemini(text, jd)
            
            if os.path.exists(path):
                os.remove(path)
    return render_template("index.html", result=result)

@app.route("/download_report", methods=["POST"])
def download_report():
    result_text = request.form.get("result_text", "No Content")
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Simple PDF Layout
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "AI Resume Analysis Report")
    
    c.setFont("Helvetica", 10)
    y = 720
    for line in result_text.splitlines():
        if y < 50:
            c.showPage()
            y = 750
        # Basic text wrapping
        c.drawString(50, y, line[:100])
        y -= 15
        
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Resume_Analysis.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)