// Get references to DOM elements
const questionForm = document.getElementById('questionForm');
const generateQuestionsBtn = document.getElementById('generateQuestionsBtn'); // New: reference to the button itself
const questionButtonText = generateQuestionsBtn.querySelector('.button-text');
const questionSpinner = generateQuestionsBtn.querySelector('.spinner');

const questionsOutputDiv = document.getElementById('questionsOutput');
const questionsContentDiv = document.getElementById('questionsContent');
const errorDiv = document.getElementById('error');

const behavioralQuestionSelect = document.getElementById('behavioralQuestionSelect');
const customBehavioralQuestion = document.getElementById('customBehavioralQuestion');
const generateStarGuideBtn = document.getElementById('generateStarGuideBtn'); // New: reference to the button itself
const starButtonText = generateStarGuideBtn.querySelector('.button-text');
const starSpinner = generateStarGuideBtn.querySelector('.spinner');

const starGuideOutputDiv = document.getElementById('starGuideOutput');
const starGuideContentDiv = document.getElementById('starGuideContent');
const starErrorDiv = document.getElementById('starError');

let fullResumeText = ""; 

// Helper function to show loading state
function showLoading(button, textSpan, spinner) {
    button.disabled = true;
    textSpan.classList.add('hidden');
    spinner.classList.remove('hidden');
    // Hide previous outputs/errors
    questionsOutputDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    starGuideOutputDiv.classList.add('hidden');
    starErrorDiv.classList.add('hidden');
}

// Helper function to hide loading state
function hideLoading(button, textSpan, spinner) {
    button.disabled = false;
    textSpan.classList.remove('hidden');
    spinner.classList.add('hidden');
}

// --- Event Listener for Question Generation Form ---
questionForm.addEventListener('submit', async (e) => {
    e.preventDefault(); 
    
    showLoading(generateQuestionsBtn, questionButtonText, questionSpinner);
    questionsContentDiv.innerHTML = '';
    behavioralQuestionSelect.innerHTML = '<option value="">-- Select a Question --</option>';

    const formData = new FormData(questionForm);

    try {
        const response = await fetch('/generate_questions', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            questionsContentDiv.innerHTML = data.questions.replace(/\n/g, '<br>');
            questionsOutputDiv.classList.remove('hidden');

            const behavioralSectionMatch = data.questions.match(/## Behavioral Questions\n- ([\s\S]*?)(?=(##|$))/i);
            if (behavioralSectionMatch && behavioralSectionMatch[1]) {
                const behavioralQuestions = behavioralSectionMatch[1].split('\n- ').filter(q => q.trim() !== '');
                behavioralQuestions.forEach(q => {
                    const option = document.createElement('option');
                    option.value = q.trim();
                    option.textContent = q.trim();
                    behavioralQuestionSelect.appendChild(option);
                });
            }
        } else {
            errorDiv.textContent = data.error || 'An unknown error occurred.';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        errorDiv.textContent = 'Network error or server unreachable.';
        errorDiv.classList.remove('hidden');
    } finally {
        hideLoading(generateQuestionsBtn, questionButtonText, questionSpinner);
    }
});

// --- Event Listener for STAR Method Guide Button ---
generateStarGuideBtn.addEventListener('click', async () => {
    showLoading(generateStarGuideBtn, starButtonText, starSpinner);
    starGuideContentDiv.innerHTML = '';

    let selectedQuestion = behavioralQuestionSelect.value;
    if (!selectedQuestion && customBehavioralQuestion.value.trim() !== "") {
        selectedQuestion = customBehavioralQuestion.value.trim();
    }

    if (!selectedQuestion) {
        starErrorDiv.textContent = 'Please select a behavioral question or type your own.';
        starErrorDiv.classList.remove('hidden');
        hideLoading(generateStarGuideBtn, starButtonText, starSpinner);
        return;
    }

    try {
        const response = await fetch('/star_guide', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: selectedQuestion, resume_text: fullResumeText })
        });

        const data = await response.json();

        if (response.ok) {
            starGuideContentDiv.innerHTML = data.star_guidance.replace(/\n/g, '<br>');
            starGuideOutputDiv.classList.remove('hidden');
        } else {
            starErrorDiv.textContent = data.error || 'An unknown error occurred.';
            starErrorDiv.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        starErrorDiv.textContent = 'Network error or server unreachable.';
        starErrorDiv.classList.remove('hidden');
    } finally {
        hideLoading(generateStarGuideBtn, starButtonText, starSpinner);
    }
});