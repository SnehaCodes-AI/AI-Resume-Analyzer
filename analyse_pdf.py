import os
import re
from google import genai
from google.genai import types

def analyze_resume_gemini(resume_content, job_description):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key, http_options=types.HttpOptions(api_version='v1'))

    prompt = f"""
    You are an expert Career Coach. Analyze this resume for a student/fresher preparing for placements.
    
    FORMATTING RULES:
    1. Start with 'MATCH_SCORE: X' (0-100).
    2. Use 'SECTION:' for main headings (OVERALL ASSESSMENT, STRENGTHS, AREAS FOR IMPROVEMENT, PLACEMENT RECOMMENDATIONS).
    3. Use 'SUBTOPIC:' for specific points under sections.
    4. NO hashtags (#) or asterisks (*). 
    5. Language should be encouraging and guidance-oriented for a student.

    RESUME: {resume_content}
    JD: {job_description}
    """

    try:
        response = client.models.generate_content(model="models/gemini-2.5-flash", contents=prompt)
        text = response.text
        score_match = re.search(r"MATCH_SCORE:\s*(\d+)", text)
        score_val = int(score_match.group(1)) if score_match else 0
        clean_text = re.sub(r"MATCH_SCORE:\s*\d+", "", text).strip()
        clean_text = clean_text.replace("*", "").replace("#", "")
        return clean_text, score_val
    except Exception as e:
        return f"Error: {str(e)}", 0