import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Get the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("API key is missing. Set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=openai_api_key)

def get_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        try:
            result = get_completion(prompt)
            return jsonify({"response": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
