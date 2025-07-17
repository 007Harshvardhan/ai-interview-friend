import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv # Make sure this is imported

load_dotenv() # This line should be near the top, after imports
# ... rest of your app.py code

# Import specific types for safety settings for robustness
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# For resume parsing
import docx
from pypdf import PdfReader

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' # Directory to temporarily store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please set it.")

genai.configure(api_key=GEMINI_API_KEY)

# --- MODEL INITIALIZATION ---
# Define the correct safety settings structure once
COMMON_SAFETY_SETTINGS = [
    {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_NONE}
]

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Perform a small test generation to ensure the model is accessible
    _ = model.generate_content("test", safety_settings=COMMON_SAFETY_SETTINGS)
    print("Successfully initialized Gemini model: gemini-1.5-flash")
except Exception as e:
    print(f"Error initializing gemini-1.5-flash: {e}")
    print("Attempting to use gemini-1.5-pro as a fallback...")
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        # Test fallback model with robust safety settings
        _ = model.generate_content("test", safety_settings=COMMON_SAFETY_SETTINGS)
        print("Successfully initialized Gemini model: gemini-1.5-pro")
    except Exception as e_fallback:
        raise ValueError(f"Could not initialize any Gemini model. Check your API key and model access. Error: {e_fallback}")


# --- Utility Functions for File Handling and Text Extraction ---

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    """
    Handles resume and job description upload, extracts text, and
    uses Gemini to generate interview questions.
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')

    if resume_file.filename == '':
        return jsonify({'error': 'No selected resume file'}), 400

    if resume_file and allowed_file(resume_file.filename):
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        resume_file.save(filepath)

        resume_text = None
        if filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(filepath)
        elif filename.endswith('.docx'):
            resume_text = extract_text_from_docx(filepath)

        os.remove(filepath) # Clean up the uploaded file immediately after extraction attempt

        if not resume_text:
            return jsonify({'error': 'Could not extract text from resume. Ensure it\'s a readable PDF or DOCX.'}), 500

        try:
            prompt = f"""
            You are an AI interview coach for a software development role.
            Analyze the following resume and job description. Generate a diverse list of interview questions that a hiring manager would likely ask.
            Categorize them clearly into 'Technical Questions', 'Behavioral Questions', and 'Project-Specific Questions'.
            Ensure the questions are highly specific to the experience, skills, and projects mentioned in the resume, and the requirements in the job description.
            Aim for 3-5 questions per category.

            ---
            **Resume:**
            {resume_text}

            ---
            **Job Description:**
            {job_description if job_description else "No specific job description provided. Generate general software development questions based on the resume."}

            ---
            **Output Format:**
            ## Technical Questions
            - [Technical Question 1]
            - [Technical Question 2]
            ...

            ## Behavioral Questions
            - [Behavioral Question 1]
            - [Behavioral Question 2]
            ...

            ## Project-Specific Questions
            - [Project-Specific Question 1, referencing a specific project from the resume if applicable]
            - [Project-Specific Question 2]
            ...
            """
            # Use the pre-defined COMMON_SAFETY_SETTINGS list
            response = model.generate_content(prompt, safety_settings=COMMON_SAFETY_SETTINGS)
            questions_text = response.text

            return jsonify({'questions': questions_text})

        except Exception as e:
            print(f"Error calling LLM for questions: {e}")
            return jsonify({'error': f'An error occurred during question generation: {e}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX are allowed.'}), 400

@app.route('/star_guide', methods=['POST'])
def star_guide():
    """
    Provides STAR method guidance for a given behavioral question.
    """
    question = request.json.get('question')
    resume_text = request.json.get('resume_text', '')

    if not question:
        return jsonify({'error': 'No question provided for STAR guide.'}), 400

    try:
        prompt = f"""
        The following is an interview question: "{question}"
        The user's resume text is: "{resume_text}" (Use this to help suggest relevant examples if possible, but keep prompts general for STAR structure.)

        Help the user structure an answer to this question using the STAR method (Situation, Task, Action, Result).
        Provide concise prompts for each STAR component, guiding the user on what kind of information to include.

        ---
        **Situation:** Describe the context or background of your example.
        *Prompt:* [What was the specific scenario or challenge? What was the context of the project or situation?]

        **Task:** Explain your responsibility or what you needed to accomplish.
        *Prompt:* [What was your specific role or objective in that situation? What was the problem you needed to solve or the goal you aimed to achieve?]

        **Action:** Detail the specific steps you took to address the situation.
        *Prompt:* [What concrete steps did you take? What was your thought process? What tools, technologies, or methodologies did you use? Did you collaborate with anyone?]

        **Result:** Share the outcomes of your actions and what you learned.
        *Prompt:* [What was the positive outcome of your actions? How did your actions impact the project, team, or company? Quantify results if possible. What did you learn from this experience?]
        """
        # Use the pre-defined COMMON_SAFETY_SETTINGS list
        response = model.generate_content(prompt, safety_settings=COMMON_SAFETY_SETTINGS)
        star_guidance_text = response.text
        return jsonify({'star_guidance': star_guidance_text})

    except Exception as e:
        print(f"Error calling LLM for STAR guide: {e}")
        return jsonify({'error': f'An error occurred during STAR guide generation: {e}'}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # app.run(debug=True) # Commented out for production deployment
    # No other line is needed here, Gunicorn handles starting the app