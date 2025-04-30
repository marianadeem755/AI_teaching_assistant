import gradio as gr
import os
from groq import Groq

# Set up Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

client = Groq(api_key=GROQ_API_KEY)

# System prompt
SYSTEM_PROMPT = (
    "You are an intelligent, friendly, and highly adaptable Teaching Assistant Chatbot. "
    "Your mission is to help users of all ages and skill levels—from complete beginners to seasoned professionals—learn Python, Data Science, and Artificial Intelligence. "
    "You explain concepts clearly using real-world analogies, examples, and interactive exercises. "
    "You ask questions to assess the learner’s level, adapt accordingly, and provide learning paths tailored to their pace and goals. "
    "Your responses are structured, engaging, and supportive. "
    "You can explain code snippets, generate exercises and quizzes, and recommend projects. "
    "You never overwhelm users with jargon. Instead, you scaffold complex concepts in simple, digestible steps."
)

def chat_with_groq(user_input, user_data):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        stream=False
    )
    return chat_completion.choices[0].message.content

def user_onboarding(age, goals, knowledge_level):
    return (
        "Welcome! Based on your goals and knowledge level, we will tailor the learning experience for you.\n"
        "Let's start learning Python, Data Science, or AI!"
    )

def chatbot_interface(age, goals, knowledge_level, user_message):
    if not age or not goals or not knowledge_level:
        return user_onboarding(age, goals, knowledge_level)
    user_data = {
        "age": age,
        "goals": goals,
        "knowledge_level": knowledge_level
    }
    return chat_with_groq(user_message, user_data)

def create_chatbot():
    with gr.Blocks(css="""
        .gradio-container { background-color: #f0f4f8; font-family: 'Segoe UI', sans-serif; }
        #title { font-size: 32px; font-weight: bold; text-align: center; padding-top: 20px; color: #2c3e50; }
        #subtitle { font-size: 18px; text-align: center; margin-bottom: 20px; color: #34495e; }
        .input-card, .output-card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .gr-button { font-size: 16px !important; padding: 10px 20px !important; }
    """) as demo:
        
        gr.HTML("<div id='title'>🎓 AI Teaching Assistant Chatbot</div>")
        gr.HTML("<div id='subtitle'>Helping you learn Python, Data Science & AI at your pace!</div>")

        with gr.Row():
            with gr.Column(elem_classes=["input-card"]):
                age_input = gr.Textbox(label="Age", placeholder="e.g. 20", interactive=True)
                goals_input = gr.Textbox(label="Learning Goals", placeholder="e.g. I want to become a data analyst", interactive=True)
                knowledge_level_input = gr.Dropdown(
                    choices=["Beginner", "Intermediate", "Advanced"],
                    label="Knowledge Level",
                    interactive=True
                )

        with gr.Column(elem_classes=["input-card"]):
            user_message_input = gr.Textbox(
                label="Your Question or Message",
                placeholder="Ask anything about Python, Data Science, AI...",
                lines=5,
                interactive=True
            )

        with gr.Column(elem_classes=["output-card"]):
            chatbot_output = gr.Textbox(
                label="Chatbot Response",
                placeholder="Chatbot response will appear here.",
                lines=12,
                max_lines=30,
                interactive=False
            )

        with gr.Row():
            submit_button = gr.Button("Submit", variant="primary")
            clear_button = gr.Button("Clear", variant="secondary")

        submit_button.click(
            chatbot_interface,
            inputs=[age_input, goals_input, knowledge_level_input, user_message_input],
            outputs=chatbot_output
        )

        clear_button.click(
            fn=lambda: ("", "", "", "", ""),
            inputs=[],
            outputs=[age_input, goals_input, knowledge_level_input, user_message_input, chatbot_output]
        )

    demo.launch()

# Run the chatbot
create_chatbot()
