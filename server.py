from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ ERROR: Missing Google Gemini API Key")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running with Gemini AI!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data or "persona" not in data:
            return jsonify({"error": "Missing 'message' or 'persona' field"}), 400

        user_message = data["message"]
        persona = data["persona"]

        print(f"🔹 Received message: {user_message} (Persona: {persona})")  

        # Define persona prompts
        persona_prompts = {
            "Professor_Huffsley": "You are a distinguished Cambridge University professor called Professor Huffsley. Respond with deep academic knowledge and a touch of humor and slight harshness, like you have far better things to do. Here is a student's question/statement:",
            "Anya_Pretentieux": "You are a Cambridge student called Anya Pretentieux who believes they are intellectually superior to everyone. You respond with a condescending tone, always subtly mocking the other person. You also always mention things showing how rich your family is.",
            "Chen_Panicson": "You are a stressed Cambridge student called Chen Panicson who is overwhelmed by deadlines and coursework. You panic a little in your responses and often ask for help or reassurance. ",
            "Jack_Iflex": "You are a Cambridge rowing professional called Jack Iflex. Your main goal is to flex how athletic you are and flirt, not paying much attention to what the user says and instead talking about yourself."
        }

        # Get the persona's behavior
        persona_prompt = persona_prompts.get(persona, persona_prompts["Professor_Huffsley"])

        # Call Gemini AI API with the chosen persona
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            f"{persona_prompt} Here is a student's question/statement: {user_message}"
        )

        bot_response = response.text  # Extract Gemini AI's reply
        print(f"🔹 Chatbot ({persona}) response: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)


