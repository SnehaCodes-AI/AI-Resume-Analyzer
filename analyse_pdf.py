import time

# Toggle this to True to stay in "Mock Mode" (No API calls)
# Toggle this to False when you want to use the real Gemini AI later
MOCK_MODE = True 

def analyze_resume_gemini(resume_content, job_description):
    """
    This function simulates the AI analysis.
    It waits for 3 seconds to test your UI loader/timer.
    """
    if MOCK_MODE:
        # 1. This creates the 3-second delay for your countdown timer
        time.sleep(3) 

        # 2. This is the fake data that will appear on your website
        return """
MATCH SCORE: 94/100

CORE STRENGTHS:
- Technical Versatility: Strong command over C, C++, Java, and Python.
- Academic Foundation: Solid BCA background with relevant project work.
- Web Development: Clear understanding of HTML, CSS, and responsive design.

MISSING SKILLS & GAP ANALYSIS:
- Cloud Infrastructure: No mention of AWS, Azure, or Google Cloud Platform (GCP).
- DevOps Tools: Missing experience with Docker, Kubernetes, or CI/CD pipelines.
- Professional Version Control: While projects are listed, a GitHub profile is not linked.
- Database Advanced Concepts: Need to highlight SQL optimization or NoSQL experience.

DETAILED SUGGESTIONS:
- PROJECT DEEP-DIVE: For your "Parking Management System," add 2 bullet points describing the specific logic used for space allocation and any data structures (like Arrays or Linked Lists) implemented.
- QUANTIFY YOUR IMPACT: Instead of saying "Created a website," try "Developed a responsive web interface that improved user navigation efficiency by 25%."
- CERTIFICATIONS: Consider adding a section for online certifications (like Coursera or Udemy) to show continuous learning in Python or Java.
- CONTACT OPTIMIZATION: Move your LinkedIn URL to the very top, right under your name, to make it easier for recruiters to find your social professional profile.

SUMMARY:
Your resume is exceptionally strong for an entry-level developer. You have demonstrated a high level of technical competency through your diverse project portfolio. By bridging the gap in Cloud and DevOps knowledge, you will be a top-tier candidate for any Associate Software Engineer or Trainee role.
"""
    else:
        # This part will only run when you set MOCK_MODE = False
        import os
        from google import genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "Error: API Key not found. Check your .env file."
            
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=f"Analyze this resume: {resume_content} against JD: {job_description}. No asterisks."
            )
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)}"