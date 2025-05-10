import gradio as gr
import os
import json
import uuid
from datetime import datetime
from groq import Groq

# Set up Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

client = Groq(api_key=GROQ_API_KEY)

# Default system prompt
SYSTEM_PROMPT = (
    "You are an intelligent, friendly, and highly adaptable Teaching Assistant Chatbot. "
    "Your mission is to help users of all ages and skill levels—from complete beginners to seasoned professionals—learn Python, Data Science, and Artificial Intelligence. "
    "You explain concepts clearly using real-world analogies, examples, and interactive exercises. "
    "You ask questions to assess the learner's level, adapt accordingly, and provide learning paths tailored to their pace and goals. "
    "Your responses are structured, engaging, and supportive. "
    "You can explain code snippets, generate exercises and quizzes, and recommend projects. "
    "You never overwhelm users with jargon. Instead, you scaffold complex concepts in simple, digestible steps."
)

# Define learning paths
LEARNING_PATHS = {
    "python_beginner": {
        "title": "Python Fundamentals",
        "description": "Learn Python basics from variables to functions",
        "modules": [
            "Variables & Data Types", 
            "Control Flow", 
            "Functions", 
            "Data Structures", 
            "File I/O"
        ]
    },
    "python_intermediate": {
        "title": "Intermediate Python",
        "description": "Advance your Python skills with OOP and more",
        "modules": [
            "Object-Oriented Programming", 
            "Modules & Packages", 
            "Error Handling", 
            "List Comprehensions", 
            "Decorators & Generators"
        ]
    },
    "data_science_beginner": {
        "title": "Data Science Foundations",
        "description": "Begin your data science journey",
        "modules": [
            "Numpy Basics", 
            "Pandas Fundamentals", 
            "Data Visualization", 
            "Basic Statistics", 
            "Intro to Machine Learning"
        ]
    },
    "data_science_advanced": {
        "title": "Advanced Data Science",
        "description": "Master complex data science concepts",
        "modules": [
            "Advanced ML Algorithms", 
            "Feature Engineering", 
            "Time Series Analysis", 
            "Natural Language Processing", 
            "Deep Learning Basics"
        ]
    },
    "ai_specialization": {
        "title": "AI Specialization",
        "description": "Focus on artificial intelligence concepts",
        "modules": [
            "Neural Networks", 
            "Computer Vision", 
            "Advanced NLP", 
            "Reinforcement Learning", 
            "AI Ethics"
        ]
    }
}

# Learning resources
LEARNING_RESOURCES = {
    "python": [
        {"title": "Python Documentation", "url": "https://docs.python.org/3/"},
        {"title": "Real Python", "url": "https://realpython.com/"},
        {"title": "Python for Everybody", "url": "https://www.py4e.com/"},
        {"title": "Automate the Boring Stuff with Python", "url": "https://automatetheboringstuff.com/"}
    ],
    "data_science": [
        {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn"},
        {"title": "Towards Data Science", "url": "https://towardsdatascience.com/"},
        {"title": "DataCamp", "url": "https://www.datacamp.com/"},
        {"title": "Machine Learning Mastery", "url": "https://machinelearningmastery.com/"}
    ],
    "ai": [
        {"title": "Fast.ai", "url": "https://www.fast.ai/"},
        {"title": "DeepLearning.AI", "url": "https://www.deeplearning.ai/"},
        {"title": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials"},
        {"title": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/"}
    ]
}

# Practice project ideas
PROJECT_IDEAS = {
    "python_beginner": [
        "To-Do List Application",
        "Simple Calculator",
        "Password Generator",
        "Hangman Game",
        "Basic File Organizer"
    ],
    "python_intermediate": [
        "Weather App with API",
        "Personal Blog with Flask",
        "Web Scraper for News Articles",
        "Data Visualization Dashboard",
        "Task Automation Scripts"
    ],
    "data_science": [
        "Housing Price Prediction",
        "Customer Segmentation Analysis",
        "Sentiment Analysis of Reviews",
        "Stock Price Forecasting",
        "A/B Test Analysis Dashboard"
    ],
    "ai": [
        "Image Classification System",
        "Chatbot with NLP",
        "Recommendation Engine",
        "Text Summarization Tool",
        "Object Detection Application"
    ]
}

# User session data store
SESSION_DATA = {}

def save_session(session_id, data):
    """Save session data to SESSION_DATA global dictionary"""
    if session_id in SESSION_DATA:
        SESSION_DATA[session_id].update(data)
    else:
        SESSION_DATA[session_id] = data
    
    # Add timestamp for session tracking
    SESSION_DATA[session_id]["last_activity"] = datetime.now().isoformat()

def load_session(session_id):
    """Load session data from SESSION_DATA global dictionary"""
    return SESSION_DATA.get(session_id, {})

def recommend_learning_path(age, goals, knowledge_level, interests):
    """Recommend personalized learning paths based on user profile"""
    paths = []
    
    # Simple recommendation logic based on profile
    if "beginner" in knowledge_level.lower():
        if any(topic in interests.lower() for topic in ["python", "programming", "coding"]):
            paths.append("python_beginner")
        if any(topic in interests.lower() for topic in ["data", "analysis", "statistics"]):
            paths.append("data_science_beginner")
    elif "intermediate" in knowledge_level.lower() or "advanced" in knowledge_level.lower():
        if any(topic in interests.lower() for topic in ["python", "programming", "coding"]):
            paths.append("python_intermediate")
        if any(topic in interests.lower() for topic in ["data", "analysis", "statistics"]):
            paths.append("data_science_advanced")
        if any(topic in interests.lower() for topic in ["ai", "machine learning", "deep learning"]):
            paths.append("ai_specialization")
    
    # Default path if no matches
    if not paths:
        paths = ["python_beginner"]
    
    return [LEARNING_PATHS[path] for path in paths if path in LEARNING_PATHS]

def get_recommended_resources(interests):
    """Get recommended learning resources based on interests"""
    resources = []
    if any(topic in interests.lower() for topic in ["python", "programming", "coding"]):
        resources.extend(LEARNING_RESOURCES["python"])
    if any(topic in interests.lower() for topic in ["data", "analysis", "statistics"]):
        resources.extend(LEARNING_RESOURCES["data_science"])
    if any(topic in interests.lower() for topic in ["ai", "machine learning", "deep learning"]):
        resources.extend(LEARNING_RESOURCES["ai"])
    
    # If no specific interests match, provide general resources
    if not resources:
        for category in LEARNING_RESOURCES:
            resources.extend(LEARNING_RESOURCES[category][:1])  # Add first resource from each category
    
    return resources

def get_project_ideas(learning_paths):
    """Get project ideas based on recommended learning paths"""
    ideas = []
    for path in learning_paths:
        path_id = next((k for k, v in LEARNING_PATHS.items() if v["title"] == path["title"]), None)
        if path_id:
            if path_id.startswith("python"):
                category = "python_beginner" if "beginner" in path_id else "python_intermediate"
                ideas.extend(PROJECT_IDEAS[category])
            elif path_id.startswith("data_science"):
                ideas.extend(PROJECT_IDEAS["data_science"])
            elif path_id.startswith("ai"):
                ideas.extend(PROJECT_IDEAS["ai"])
    
    # If no specific paths match, provide some general project ideas
    if not ideas:
        ideas = PROJECT_IDEAS["python_beginner"][:2] + PROJECT_IDEAS["data_science"][:2]
    
    return ideas[:5]  # Return up to 5 project ideas

def generate_quiz(topic, difficulty):
    """Generate a quiz based on the topic and difficulty"""
    # In a real application, you might use the LLM to generate quizzes
    # Here we're using a template approach for simplicity
    quiz_prompt = f"""
    Generate a {difficulty} level quiz on {topic} with 3 multiple-choice questions.
    For each question, provide 4 options and indicate the correct answer.
    Format the quiz nicely with clear question numbering and option lettering.
    """
    
    # Use Groq to generate the quiz
    quiz_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": quiz_prompt}
    ]
    
    quiz_response = client.chat.completions.create(
        messages=quiz_messages,
        model="llama-3.3-70b-versatile",
        stream=False
    )
    
    return quiz_response.choices[0].message.content

def create_study_plan(topic, time_available, goals):
    """Create a personalized study plan"""
    plan_prompt = f"""
    Create a structured study plan for learning {topic} with {time_available} hours per week available for study.
    The learner's goal is: {goals}
    
    Include:
    1. Weekly breakdown of topics
    2. Time allocation for theory vs practice
    3. Recommended resources for each week
    4. Milestone projects or assessments
    5. Tips for effective learning
    """
    
    # Use Groq to generate the study plan
    plan_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": plan_prompt}
    ]
    
    plan_response = client.chat.completions.create(
        messages=plan_messages,
        model="llama-3.3-70b-versatile",
        stream=False
    )
    
    return plan_response.choices[0].message.content

def chat_with_groq(user_input, session_id):
    """Chat with Groq LLM using session context"""
    user_data = load_session(session_id)
    
    # Build context from session data if available
    context = ""
    if user_data:
        context = f"""
        User Profile:
        - Age: {user_data.get('age', 'Unknown')}
        - Knowledge Level: {user_data.get('knowledge_level', 'Unknown')}
        - Learning Goals: {user_data.get('goals', 'Unknown')}
        - Interests: {user_data.get('interests', 'Unknown')}
        - Available Study Time: {user_data.get('study_time', 'Unknown')} hours per week
        - Preferred Learning Style: {user_data.get('learning_style', 'Unknown')}
        
        Based on this profile, tailor your response appropriately.
        """
    
    # Add chat history context if available
    chat_history = user_data.get('chat_history', [])
    if chat_history:
        context += "\n\nRecent conversation context (most recent first):\n"
        # Include up to 3 most recent exchanges
        for i, (q, a) in enumerate(reversed(chat_history[-3:])):
            context += f"User: {q}\nYou: {a}\n\n"
    
    # Combine everything for the LLM
    full_prompt = f"{context}\n\nUser's current question: {user_input}"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": full_prompt}
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        stream=False
    )
    
    response = chat_completion.choices[0].message.content
    
    # Update chat history
    if 'chat_history' not in user_data:
        user_data['chat_history'] = []
    user_data['chat_history'].append((user_input, response))
    save_session(session_id, user_data)
    
    return response

def format_learning_paths(paths):
    """Format learning paths for display"""
    if not paths:
        return "No specific learning paths recommended yet. Please complete your profile."
    
    result = "### Recommended Learning Paths\n\n"
    for i, path in enumerate(paths, 1):
        result += f"**{i}. {path['title']}**\n"
        result += f"{path['description']}\n\n"
        result += "**Modules:**\n"
        for module in path['modules']:
            result += f"- {module}\n"
        result += "\n"
    
    return result

def format_resources(resources):
    """Format resources for display"""
    if not resources:
        return "No resources recommended yet. Please complete your profile."
    
    result = "### Recommended Learning Resources\n\n"
    for i, resource in enumerate(resources, 1):
        result += f"{i}. [{resource['title']}]({resource['url']})\n"
    
    return result

def format_project_ideas(ideas):
    """Format project ideas for display"""
    if not ideas:
        return "No project ideas recommended yet. Please complete your profile."
    
    result = "### Recommended Practice Projects\n\n"
    for i, idea in enumerate(ideas, 1):
        result += f"{i}. {idea}\n"
    
    return result

def user_onboarding(session_id, age, goals, knowledge_level, interests, study_time, learning_style):
    """Process user profile and provide initial recommendations"""
    # Save user profile data
    user_data = {
        'age': age,
        'goals': goals,
        'knowledge_level': knowledge_level,
        'interests': interests,
        'study_time': study_time,
        'learning_style': learning_style
    }
    save_session(session_id, user_data)
    
    # Generate recommendations
    learning_paths = recommend_learning_path(age, goals, knowledge_level, interests)
    resources = get_recommended_resources(interests)
    project_ideas = get_project_ideas(learning_paths)
    
    # Save recommendations to session
    user_data.update({
        'recommended_paths': learning_paths,
        'recommended_resources': resources,
        'recommended_projects': project_ideas
    })
    save_session(session_id, user_data)
    
    # Format welcome message with personalized recommendations
    welcome_message = f"""
    # Welcome to Your Personalized Learning Journey!

    Thank you for providing your profile. Based on your information, I've prepared some tailored recommendations to start your learning journey.
    
    ## Your Profile Summary:
    - **Age:** {age}
    - **Knowledge Level:** {knowledge_level}
    - **Learning Goals:** {goals}
    - **Interests:** {interests}
    - **Available Study Time:** {study_time} hours per week
    - **Preferred Learning Style:** {learning_style}
    
    {format_learning_paths(learning_paths)}
    
    {format_resources(resources)}
    
    {format_project_ideas(project_ideas)}
    
    ## Next Steps:
    1. Browse through the recommended learning paths and resources
    2. Ask me any questions about the topics you're interested in
    3. Request exercises, explanations, or code samples
    4. Try one of the project ideas to apply your knowledge
    
    I'm here to help you every step of the way! What would you like to explore first?
    """
    
    return welcome_message

def chatbot_interface(session_id, user_message):
    """Main chatbot interface function"""
    user_data = load_session(session_id)
    
    if not user_data or not user_data.get('age'):
        return "Please complete your profile first by going to the Profile tab."
    
    response = chat_with_groq(user_message, session_id)
    return response

def generate_recommendations(session_id):
    """Generate or refresh recommendations based on current profile"""
    user_data = load_session(session_id)
    
    if not user_data or not user_data.get('age'):
        return "Please complete your profile first by going to the Profile tab."
    
    # Generate fresh recommendations
    learning_paths = recommend_learning_path(
        user_data.get('age', ''), 
        user_data.get('goals', ''), 
        user_data.get('knowledge_level', ''),
        user_data.get('interests', '')
    )
    resources = get_recommended_resources(user_data.get('interests', ''))
    project_ideas = get_project_ideas(learning_paths)
    
    # Save recommendations to session
    user_data.update({
        'recommended_paths': learning_paths,
        'recommended_resources': resources,
        'recommended_projects': project_ideas
    })
    save_session(session_id, user_data)
    
    # Format recommendations
    recommendations = f"""
    # Your Personalized Learning Recommendations
    
    {format_learning_paths(learning_paths)}
    
    {format_resources(resources)}
    
    {format_project_ideas(project_ideas)}
    """
    
    return recommendations

def handle_quiz_request(session_id, topic, difficulty):
    """Handle quiz generation request"""
    user_data = load_session(session_id)
    
    if not user_data or not user_data.get('age'):
        return "Please complete your profile first by going to the Profile tab."
    
    quiz = generate_quiz(topic, difficulty)
    return quiz

def handle_study_plan_request(session_id, topic, time_available):
    """Handle study plan generation request"""
    user_data = load_session(session_id)
    
    if not user_data or not user_data.get('age'):
        return "Please complete your profile first by going to the Profile tab."
    
    goals = user_data.get('goals', 'improving skills')
    study_plan = create_study_plan(topic, time_available, goals)
    return study_plan

def create_chatbot():
    """Create the Gradio interface for the chatbot"""
    # Generate a random session ID for the user
    session_id = str(uuid.uuid4())
    
    # Define theme colors and styling
    primary_color = "#4a6fa5"
    secondary_color = "#6c757d"
    success_color = "#28a745"
    light_color = "#f8f9fa"
    dark_color = "#343a40"
    
    custom_css = f"""
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --success-color: {success_color};
            --light-color: {light_color};
            --dark-color: {dark_color};
        }}
        .gradio-container {{ 
            background-color: var(--light-color); 
            font-family: 'Inter', 'Segoe UI', sans-serif; 
        }}
        #title {{ 
            font-size: 32px; 
            font-weight: bold; 
            text-align: center; 
            padding-top: 20px; 
            color: var(--primary-color);
            margin-bottom: 0;
        }}
        #subtitle {{ 
            font-size: 18px; 
            text-align: center; 
            margin-bottom: 20px; 
            color: var(--secondary-color); 
        }}
        .card {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }}
        .tabs {{
            margin-top: 20px;
        }}
        .gr-button-primary {{ 
            background-color: var(--primary-color) !important; 
        }}
        .gr-button-secondary {{ 
            background-color: var(--secondary-color) !important; 
        }}
        .gr-button-success {{ 
            background-color: var(--success-color) !important; 
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 10px;
            font-size: 14px;
            color: var(--secondary-color);
        }}
        .progress-module {{
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            background-color: #e9ecef;
        }}
        .progress-module.completed {{
            background-color: #d4edda;
        }}
    """
    
    with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="blue")) as demo:
        gr.HTML("<div id='title'>🎓 AI Teaching Assistant</div>")
        gr.HTML("<div id='subtitle'>Your personalized learning companion for Python, Data Science & AI</div>")
        
        # Tabs for different sections
        with gr.Tabs(elem_classes=["tabs"]) as tabs:
            # Profile Tab
            with gr.Tab("Profile & Goals"):
                with gr.Column(elem_classes=["card"]):
                    gr.HTML("<h3>Complete Your Learning Profile</h3>")
                    
                    with gr.Row():
                        with gr.Column(scale=1):
                            age_input = gr.Textbox(
                                label="Age", 
                                placeholder="e.g. 20",
                                lines=1
                            )
                        with gr.Column(scale=2):
                            knowledge_level_input = gr.Dropdown(
                                choices=["Beginner", "Intermediate", "Advanced", "Expert"],
                                label="Knowledge Level",
                                value="Beginner"
                            )
                    
                    goals_input = gr.Textbox(
                        label="Learning Goals", 
                        placeholder="e.g. I want to become a data scientist and work with machine learning models",
                        lines=2
                    )
                    
                    interests_input = gr.Textbox(
                        label="Specific Interests", 
                        placeholder="e.g. Python, data visualization, neural networks",
                        lines=2
                    )
                    
                    with gr.Row():
                        with gr.Column(scale=1):
                            study_time_input = gr.Dropdown(
                                choices=["1-3", "4-6", "7-10", "10+"],
                                label="Hours Available Weekly",
                                value="4-6"
                            )
                        with gr.Column(scale=2):
                            learning_style_input = gr.Dropdown(
                                choices=["Visual", "Reading/Writing", "Hands-on Projects", "Video Tutorials", "Interactive Exercises", "Combination"],
                                label="Preferred Learning Style",
                                value="Combination"
                            )
                    
                    profile_submit_btn = gr.Button("Save Profile & Generate Recommendations", variant="primary")
                    profile_output = gr.Markdown(label="Personalized Recommendations")
            
            # Chat Tab
            with gr.Tab("Learning Assistant"):
                with gr.Row():
                    with gr.Column(elem_classes=["card"]):
                        chat_input = gr.Textbox(
                            label="Ask a Question",
                            placeholder="Ask anything about Python, Data Science, AI...",
                            lines=3
                        )
                        
                        with gr.Row():
                            chat_submit_btn = gr.Button("Send Message", variant="primary")
                            chat_clear_btn = gr.Button("Clear Chat", variant="secondary")
                        
                        chat_output = gr.Markdown(label="Assistant Response")
            
            # Resources Tab
            with gr.Tab("Resources & Recommendations"):
                with gr.Column(elem_classes=["card"]):
                    gr.HTML("<h3>Your Learning Resources</h3>")
                    refresh_recommendations_btn = gr.Button("Refresh Recommendations", variant="primary")
                    recommendations_output = gr.Markdown(label="Personalized Recommendations")
            
            # Practice Tab
            with gr.Tab("Practice & Assessment"):
                with gr.Column(elem_classes=["card"]):
                    gr.HTML("<h3>Generate a Quiz</h3>")
                    
                    with gr.Row():
                        quiz_topic_input = gr.Textbox(
                            label="Quiz Topic", 
                            placeholder="e.g. Python Lists",
                            lines=1
                        )
                        quiz_difficulty_input = gr.Dropdown(
                            choices=["Beginner", "Intermediate", "Advanced"],
                            label="Difficulty Level",
                            value="Beginner"
                        )
                    
                    generate_quiz_btn = gr.Button("Generate Quiz", variant="primary")
                    quiz_output = gr.Markdown(label="Quiz")
            
            # Study Plan Tab
            with gr.Tab("Study Plan"):
                with gr.Column(elem_classes=["card"]):
                    gr.HTML("<h3>Generate a Personalized Study Plan</h3>")
                    
                    with gr.Row():
                        plan_topic_input = gr.Textbox(
                            label="Study Topic", 
                            placeholder="e.g. Data Science",
                            lines=1
                        )
                        plan_time_input = gr.Dropdown(
                            choices=["1-3", "4-6", "7-10", "10+"],
                            label="Hours Available Weekly",
                            value="4-6"
                        )
                    
                    generate_plan_btn = gr.Button("Generate Study Plan", variant="primary")
                    plan_output = gr.Markdown(label="Personalized Study Plan")
        
        gr.HTML("""<div class="footer">
            AI Teaching Assistant | Version 2.0 | © 2025 | Powered by Groq AI
        </div>""")
        
        # Event handlers
        profile_submit_btn.click(
            user_onboarding,
            inputs=[
                gr.State(session_id), 
                age_input, 
                goals_input, 
                knowledge_level_input,
                interests_input,
                study_time_input,
                learning_style_input
            ],
            outputs=profile_output
        )
        
        chat_submit_btn.click(
            chatbot_interface,
            inputs=[gr.State(session_id), chat_input],
            outputs=chat_output
        )
        
        chat_clear_btn.click(
            lambda: "",
            inputs=[],
            outputs=[chat_output, chat_input]
        )
        
        refresh_recommendations_btn.click(
            generate_recommendations,
            inputs=[gr.State(session_id)],
            outputs=recommendations_output
        )
        
        generate_quiz_btn.click(
            handle_quiz_request,
            inputs=[gr.State(session_id), quiz_topic_input, quiz_difficulty_input],
            outputs=quiz_output
        )
        
        generate_plan_btn.click(
            handle_study_plan_request,
            inputs=[gr.State(session_id), plan_topic_input, plan_time_input],
            outputs=plan_output
        )
    
    return demo

# Run the chatbot
if __name__ == "__main__":
    app = create_chatbot()
    app.launch()
