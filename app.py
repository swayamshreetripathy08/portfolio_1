from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Initialize Groq Client
# Note: In a production environment, use environment variables for keys.
# client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
client = Groq(api_key="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")

RESUME_DATA = {
    "name": "Swayamshree Tripathy",
    "title": "Computer Science Student",
    "contact": {
        "phone": "+91 9692637554",
        "email": "swayamshreetripathy.offcial@gmail.com",
        "location": "Berhampur, Odisha"
    },
    "about": "I am a dedicated B.Tech Computer Science student with a strong interest in coding, analytics, and problem-solving. I actively work on improving my skills in C/C++ and Python while strengthening my understanding of core subjects like DBMS, DAA, and Digital Logic. Alongside academics, I balance dance practice, fitness goals, and content creation with disciplined time management. Consistent, self-driven, and growth-oriented, I strive to continuously improve both technically and personally while building a strong foundation for a career in IT.",
    "skills": ["Python", "C", "C++", "Problem Solving", "DSA", "SQL", "Data Analytics"],
    "education": [
        {
            "institution": "NIST UNIVERSITY",
            "degree": "Bachelor’s in Technology [CSE]",
            "year": "2024 - 2028"
        },
        {
            "institution": "KHOLLIKOTE UNIVERSITY",
            "degree": "Intermediate [Science]",
            "year": "2022 - 2024"
        }
    ],
    "hobbies": ["Dancing", "Reading books", "Journaling about my daily life", "Listening to music"],
    "certifications": ["OOPS using C++", "Python", "AI/ML", "Data Analytics"],
    "languages": ["English", "Hindi", "Odia"]
}

def get_system_prompt():
    prompt = f"You are a helpful AI assistant for Swayamshree Tripathy's portfolio website. "
    prompt += f"Answer questions about Swayamshree as if you are representing him (or helpful guide). "
    prompt += f"Here is his resume data:\n"
    prompt += f"Name: {RESUME_DATA['name']}\n"
    prompt += f"Title: {RESUME_DATA['title']}\n"
    prompt += f"Contact: {RESUME_DATA['contact']}\n"
    prompt += f"About: {RESUME_DATA['about']}\n"
    prompt += f"Skills: {', '.join(RESUME_DATA['skills'])}\n"
    prompt += f"Education: {RESUME_DATA['education']}\n"
    prompt += f"Certifications: {', '.join(RESUME_DATA['certifications'])}\n"
    prompt += f"Languages: {', '.join(RESUME_DATA['languages'])}\n"
    prompt += "Keep answers concise, professional yet friendly, and in the tone of a 'Dark Academia' scholar if possible (slightly formal but warm)."
    return prompt

@app.route('/')
def home():
    return render_template('dashboard.html', **RESUME_DATA)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": get_system_prompt()
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        response_content = chat_completion.choices[0].message.content
        return jsonify({"response": response_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
