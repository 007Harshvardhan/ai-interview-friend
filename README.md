# 🚀 AI Interview Coach: Your Personal Interview AI

Welcome to the AI Interview Coach! This cutting-edge tool leverages the power of Artificial Intelligence to help software developers ace their interviews by generating tailored questions and guiding them through the STAR method.

Prepare to revolutionize your interview prep!

---

## ✨ Live Demo

Experience the AI Interview Coach live on Render:
👉 **[https://ai-interview-friend.onrender.com/](https://ai-interview-friend.onrender.com/)** 👈

---

## 🌟 Features

* **Intelligent Resume & Job Description Analysis:** Upload your resume and paste a job description. The AI will analyze both to understand your profile and the role's requirements.
* **AI-Powered Question Generation:** Get a diverse set of interview questions (Technical, Behavioral, Project-Specific) specifically tailored to your experience and the target role, powered by Google Gemini.
* **STAR Method Guidance:** For behavioral questions, receive step-by-step prompts to structure your answers using the Situation, Task, Action, Result (STAR) method.
* **Dynamic & Futuristic UI:** Immerse yourself in a sleek, responsive interface featuring an advanced "AI video game" theme with animated backgrounds, glowing elements, and professional typography.
* **Secure API Key Handling:** Your sensitive API keys are securely managed via environment variables during deployment.

---

## 🛠️ Technologies Used

* **Backend:**
    * [Python 3.9+](https://www.python.org/)
    * [Flask](https://flask.palletsprojects.com/) (Web Framework)
    * [Google Generative AI SDK](https://ai.google.dev/gemini-api/docs/get-started/python) (for Gemini API interaction)
    * `python-docx`, `pypdf` (for resume text extraction)
    * `python-dotenv` (for local environment variables)
    * [Gunicorn](https://gunicorn.org/) (Production WSGI Server)
* **Frontend:**
    * HTML5, Advanced CSS3 (with complex gradients, animations, and responsive design), JavaScript
    * [Google Fonts (Inter, Orbitron)](https://fonts.google.com/) (for professional, futuristic typography)
* **Deployment:**
    * [Git](https://git-scm.com/)
    * [GitHub](https://github.com/)
    * [Render.com](https://render.com/) (Platform as a Service for live deployment)

---

## 🚀 Getting Started (Local Setup)

To run the AI Interview Coach on your local machine:

### Prerequisites

* **Python 3.9+**: [Download & Install Python](https://www.python.org/downloads/)
* **Git**: [Download & Install Git](https://git-scm.com/downloads)
* **Google Gemini API Key**:
    1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    2.  Sign in with your Google account.
    3.  Click "Create API key in new project" (or select an existing project).
    4.  **Copy your generated API key immediately.**

### Installation & Run

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/007Harshvardhan/ai-interview-friend.git](https://github.com/007Harshvardhan/ai-interview-friend.git)
    cd ai-interview-friend
    ```
    *(Note: Ensure you clone the correct repository where your project resides.)*

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    # macOS/Linux:
    source venv/bin/activate
    # Windows:
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # Ensure gunicorn is also installed:
    pip install gunicorn
    ```
    *(If you just ran `pip freeze > requirements.txt`, `gunicorn` should already be in it. If not, run `pip install gunicorn` and then `pip freeze > requirements.txt` again.)*

4.  **Create a `.env` file:**
    * In the root of your project directory, create a file named `.env`.
    * Add your Gemini API Key:
        ```
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```
        **Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual key.**

5.  **Verify `app.py` for Local Run:**
    * Open `app.py`.
    * Ensure the `if __name__ == '__main__':` block looks like this for local development:
        ```python
        if __name__ == '__main__':
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            app.run(debug=True) # Keep this line for local testing
        ```

6.  **Run the Flask Application:**
    ```bash
    python app.py
    ```
    The server will start, usually on `http://127.0.0.1:5000`.

7.  **Access in Browser:**
    * Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## 🌐 Deployment to Render.com

This project is configured for seamless deployment on [Render.com](https://render.com/).

### Deployment Preparation

1.  **Verify `requirements.txt`:** Ensure it includes `gunicorn` and all other project dependencies.
    ```bash
    pip freeze > requirements.txt
    ```

2.  **Create/Verify `Procfile`:** In your project root, create a file named `Procfile` (no extension) with this content:
    ```
    web: python -m gunicorn app:app
    ```

3.  **Modify `app.py` for Production:** Comment out `app.run(debug=True)`:
    ```python
    if __name__ == '__main__':
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # app.run(debug=True) # Commented out for production deployment
    ```
    Ensure `load_dotenv()` is at the very top of `app.py` after imports.

4.  **Create/Update `.gitignore`:** Ensure it contains:
    ```
    .env
    venv/
    __pycache__/
    *.pyc
    uploads/
    ```

5.  **Commit and Push to GitHub:**
    ```bash
    git add .
    git commit -m "Prepare for Render deployment"
    git push origin main
    ```

### Deploying on Render

1.  **Sign Up/Log In to Render:** Go to [https://render.com/](https://render.com/) and sign up or log in with your GitHub account.
2.  **Create New Web Service:** From your Render dashboard, click "New" -> "Web Service".
3.  **Connect Repository:** Select your `007Harshvardhan/ai-interview-friend` GitHub repository.
4.  **Configure Service Details:**
    * **Name:** A unique name (e.g., `ai-interview-friend`).
    * **Branch:** `main`.
    * **Root Directory:** Leave blank.
    * **Runtime:** `Python 3`.
    * **Build Command:** `pip install -r requirements.txt`.
    * **Start Command:** `python -m gunicorn app:app`.
    * **Instance Type:** `Free`.
5.  **Add Environment Variables:**
    * **Key:** `GEMINI_API_KEY`, **Value:** Your actual Google Gemini API Key.
    * **Key:** `FLASK_ENV`, **Value:** `production`.
6.  **Create Web Service:** Click the button to initiate deployment.

Monitor the build logs on Render. Once deployed, your app will be live at the URL provided by Render!

---

## 👨‍💻 Credits

Developed with passion by **Harsh Vardhan** in 2025.

Connect with me on [LinkedIn](https://www.linkedin.com/in/your-linkedin-profile)! *(Remember to update this link with your actual profile!)*

---

## 📄 License

This project is open-sourced under the MIT License. See the [LICENSE](LICENSE) file for details.
