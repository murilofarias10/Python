import os
from flask import Flask, render_template, request, jsonify
from storage import diff_store
from werkzeug.utils import secure_filename
import random
import PyPDF2
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv(override=True)

# Setup your Azure Inference Client
class SimpleAgent:
    def __init__(self, system_prompt=None):
        default_prompt = (
            "You are an expert reviewer. "
            "Analyze the provided content and give helpful, constructive feedback. "
            "Your feedback should be clear, insightful, and written in 3 to 5 lines maximum."
        )
        self.system_prompt = system_prompt if system_prompt else default_prompt
        self.token = os.environ["GITHUB_TOKEN"]
        self.endpoint = "https://models.github.ai/inference"
        self.model_name = "mistral-ai/Mistral-small"
        self.client = ChatCompletionsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.token))

    def run(self, user_input):
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                UserMessage(content=user_input)
            ]
            response = self.client.complete(model=self.model_name, messages=messages)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error in generating LLM output: {str(e)}"

def create_agent(system_prompt=None):
    return SimpleAgent(system_prompt)

# Create your updated expert agent
agent = create_agent()

# --- Clean Invalid UTF-8 Characters ---
def clean_invalid_utf8(text):
    """Clean text from any invalid UTF-8 characters and surrogate pairs"""
    if not text:
        return ""
    # Filter out surrogate pairs and other problematic characters
    return ''.join(char for char in text if 0 < ord(char) < 0xD800 or 0xDFFF < ord(char) < 0x10000)

# --- Validate File, handling pdf and txt ---
def read_file(file_path):
    try:
        if not file_path:
            return "Error: Please upload a valid file."
            
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            return content if content else "Error: Empty file."
        elif file_ext == '.pdf':
            try:
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    content = ''
                    for page in pdf_reader.pages:
                        content += page.extract_text() + '\n'
                return content.strip() if content.strip() else "Error: Empty PDF file."
            except Exception as e:
                return f"Error reading PDF file: {str(e)}"
        else:
            return "Error: Please upload a valid .txt or .pdf file."
    except Exception as e:
        return f"Error reading file: {str(e)}"

# --- Generate Quiz Questions ---
def create_quiz_questions(content):
    if not content or isinstance(content, str) and content.startswith("Error"):
        return "Could not generate question. Please check your file."

    sentences = [s.strip() for s in content.split('\n') if len(s.strip()) > 20 and ':' not in s]

    if not sentences:
        return "Not enough content to generate a question."

    all_words = set(word.lower() for sentence in sentences for word in sentence.split()
                    if len(word) > 3 and not word.isupper())

    if len(all_words) == 0:
        return "Could not generate words for options."

    sentence = random.choice(sentences)

    words = [word for word in sentence.split()
             if len(word) > 3 and not word.isupper()
             and word.lower() not in ['they', 'their', 'them', 'like', 'with', 'from']]

    if not words:
        return "Could not generate a valid question from the content."

    chosen_word = random.choice(words)
    blank_sentence = sentence.replace(chosen_word, "_____", 1)

    similar_words = [w for w in all_words
                     if len(w) >= len(chosen_word) - 2 and len(w) <= len(chosen_word) + 2 and w != chosen_word.lower()]

    if len(similar_words) < 2:
        return "Could not generate enough options."

    wrong_options = random.sample(similar_words, 2)
    options = [chosen_word] + wrong_options
    random.shuffle(options)

    complete_sentence = sentence.replace(chosen_word, chosen_word.capitalize(), 1)
    return {
        "question": blank_sentence,
        "options": [f"Option {chr(97 + i)}: {opt}" for i, opt in enumerate(options)],
        "answer": chosen_word,
        "correct_option": f"Option {chr(97 + options.index(chosen_word))}: {chosen_word}",
        "complete_sentence": complete_sentence
    }

# --- Generate IA Response ---
def generate_ia_response(complete_sentence):
    """
    Queries the AI agent with the complete sentence and returns the IA's response.
    """
    try:
        if not complete_sentence or complete_sentence.strip() == "":
            return "No complete sentence available to generate AI response."

        ia_response = agent.run(f"Provide detailed information about: {complete_sentence}")
        ia_response = clean_invalid_utf8(ia_response)
        return ia_response
    except Exception as e:
        return f"Error processing IA response: {str(e)}"

# --- Process File and Generate Output ---
def process_file(file_path):
    """
    Reads the file, generates a question, and returns the question data.
    """
    content = read_file(file_path)
    if isinstance(content, str) and content.startswith("Error"):
        return {"error": content}

    question = create_quiz_questions(content)
    if isinstance(question, str):
        return {"error": question}

    return question

# Configure Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

# Store uploaded files in memory for reuse
uploaded_files = {}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to validate file content
def validate_file(file):
    """Validate file size and content"""
    if not file or file.filename == '':
        return "No file selected"
        
    if not allowed_file(file.filename):
        return "File type not allowed. Please upload a .txt or .pdf file"
    
    # Check if file is empty
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if file_size == 0:
        return "File is empty"
    
    if file_size > MAX_CONTENT_LENGTH:
        return f"File too large. Maximum size is {MAX_CONTENT_LENGTH/1024/1024}MB"
    
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Validate file
    error = validate_file(file)
    if error:
        return jsonify({"error": error}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Generate a unique file ID and store the path
        file_id = str(random.randint(10000, 99999))
        uploaded_files[file_id] = file_path
        
        # Generate a unique session ID for this user
        session_id = str(random.randint(100000, 999999))
        
        # Store file_id in diff_store instead of session
        diff_store.set(session_id, 'current_file_id', file_id)
        
        # Process the file and generate a question
        question_data = process_file(file_path)
        
        if "error" in question_data:
            return jsonify({"error": question_data["error"]}), 400
        
        # Store the complete sentence in diff_store for AI response later
        diff_store.set(session_id, 'complete_sentence', question_data['complete_sentence'])
        
        # Add file_id and session_id to the response
        question_data['file_id'] = file_id
        question_data['session_id'] = session_id
        
        response = jsonify(question_data)
        
        # Set session_id cookie if not already set
        if 'session_id' not in request.cookies:
            response.set_cookie('session_id', session_id, max_age=3600)
            
        return response, 200
    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/generate-another', methods=['POST'])
def generate_another():
    # Get session_id from request body or cookie
    data = request.get_json() or {}
    session_id = data.get('session_id') or request.cookies.get('session_id')
    if not session_id:
        return jsonify({"error": "Session expired. Please upload a file again."}), 400
    
    # Get the current file ID from diff_store
    file_id = diff_store.get(session_id, 'current_file_id')
    
    if not file_id or file_id not in uploaded_files:
        return jsonify({"error": "No file available. Please upload a file first."}), 400
    
    try:
        # Get the file path and process it again
        file_path = uploaded_files[file_id]
        
        # Check if the file still exists on disk
        if not os.path.exists(file_path):
            return jsonify({"error": "The uploaded file no longer exists. Please upload a file again."}), 400
        
        # Process the file and generate a new question
        question_data = process_file(file_path)
        
        if "error" in question_data:
            return jsonify({"error": question_data["error"]}), 400
        
        # Store the complete sentence in diff_store for AI response later
        diff_store.set(session_id, 'complete_sentence', question_data['complete_sentence'])
        
        # Add file_id to the response
        question_data['file_id'] = file_id
        question_data['session_id'] = session_id
        
        return jsonify(question_data), 200
    except Exception as e:
        return jsonify({"error": f"Error generating question: {str(e)}"}), 500

@app.route('/ai-response', methods=['POST'])
def ai_response():
    # Get session_id from request body or cookie
    data = request.get_json() or {}
    session_id = data.get('session_id') or request.cookies.get('session_id')
    if not session_id:
        return jsonify({"error": "Session expired. Please upload a file again."}), 400
    
    # Get the current file ID from diff_store
    file_id = diff_store.get(session_id, 'current_file_id')
    
    if not file_id or file_id not in uploaded_files:
        return jsonify({"error": "No file available. Please upload a file first."}), 400
    
    # Get the file path and check if it exists on disk
    file_path = uploaded_files[file_id]
    if not os.path.exists(file_path):
        return jsonify({"error": "The uploaded file no longer exists. Please upload a file again."}), 400
    
    complete_sentence = diff_store.get(session_id, 'complete_sentence', '')
    
    if not complete_sentence:
        return jsonify({"error": "No sentence available"}), 400
    
    try:
        response = generate_ia_response(complete_sentence)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": f"Error generating AI response: {str(e)}"}), 500

@app.route('/clear-session', methods=['POST'])
def clear_session():
    """Clear user session data when they go home"""
    # Get session_id from request body or cookie
    data = request.get_json() or {}
    session_id = data.get('session_id') or request.cookies.get('session_id')
    if session_id:
        # Get the current file ID from diff_store first
        file_id = diff_store.get(session_id, 'current_file_id')
        
        # Clean up file if it exists
        if file_id and file_id in uploaded_files:
            file_path = uploaded_files[file_id]
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                del uploaded_files[file_id]
            except Exception:
                pass  # Ignore errors when cleaning up files
        
        # Clean up diff_store after getting the file_id
        diff_store.delete(session_id)
    
    response = jsonify({"status": "success"})
    response.delete_cookie('session_id')
    return response, 200

#if __name__ == "__main__":
    #app.run(host="127.0.0.1", port=7861, debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
