import os
import gradio as gr
import random
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

#pip install azure-ai-inference
#pip install gradio
#pip install python-dotenv

# Load environment variables
load_dotenv(override=True)

# Setup your Azure Inference Client
class SimpleAgent:
    def __init__(self, system_prompt="You are an intelligent agent that generates context for quiz questions."):
        self.system_prompt = system_prompt
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
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in generating LLM output: {str(e)}"


def create_agent(system_prompt="You are an intelligent agent that generates context for quiz questions."):
    return SimpleAgent(system_prompt)

agent = create_agent()

# --- 2 Validate TXT File ---
def read_txt_file(file):
    try:
        if not file or not file.name.lower().endswith('.txt'):
            return "Error: Please upload a valid TXT file."
        with open(file.name, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content if content else "Error: Empty file."
    except Exception as e:
        return f"Error reading file: {str(e)}"

# --- 3 Generate Quiz Questions ---
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
        "correct_option": f"Option {chr(97 + options.index(chosen_word))}",
        "complete_sentence": complete_sentence
    }

# --- 4 Generate IA Response ---
def generate_ia_response(complete_sentence):
    """
    Queries the AI agent with the complete sentence and returns the IA's response.
    """
    try:
        if not complete_sentence or complete_sentence.strip() == "":
            return "No complete sentence available to generate AI response."

        ia_response = agent.run(f"Provide detailed information about: {complete_sentence}")
        ia_response = clean_invalid_utf8(ia_response)  # 💥
        return ia_response
    except Exception as e:
        return f"Error processing IA response: {str(e)}"



# --- 5 Process File and Generate Output ---
def process_file(file):
    """
    Reads the file, generates a question, and formats the output.
    """
    content = read_txt_file(file)
    if isinstance(content, str) and content.startswith("Error"):
        return content, ""

    question = create_quiz_questions(content)
    if isinstance(question, str):
        return question, ""

    output = "### Fill in the blank:\n\n"
    output += f"**{question['question']}**\n\n"
    output += "**Choose the correct answer:**\n\n"
    for option in question['options']:
        output += f"* {option}\n"

    output += f"\n<details><summary>👉 Show Answer</summary>\n\n"
    output += f"**Correct answer: {question['answer']} ({question['correct_option']})**\n\n"
    output += f"**Complete sentence:** {question['complete_sentence']}\n"
    output += "</details>\n"

    output = clean_invalid_utf8(output)  # 💥
    return output, question['complete_sentence']



# --- 6 Clean Outputs ---
def clean_outputs():
    return None, "", ""

# --- 7 Create Gradio Interface ---
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# \ud83d\udcda SmartQuiz with AI by: Murilo Farias")

        with gr.Row():
            file_input = gr.File(label="Upload TXT file", file_types=[".txt"])

        with gr.Row():
            submit_btn = gr.Button("Generate Question")
            ia_btn = gr.Button("Get AI Response")
            clean_btn = gr.Button("Clean")

        output = gr.Markdown()
        hidden_sentence = gr.Textbox(visible=False, interactive=False)
        ia_response = gr.Markdown(label="Generate AI Context")

        submit_btn.click(fn=process_file, inputs=[file_input], outputs=[output, hidden_sentence])
        ia_btn.click(fn=generate_ia_response, inputs=[hidden_sentence], outputs=[ia_response])
        clean_btn.click(fn=clean_outputs, inputs=[], outputs=[file_input, output, ia_response])

    return demo

# --- 8 Launch the Application ---
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7861)