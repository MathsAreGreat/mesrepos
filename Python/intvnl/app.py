import json
from flask import Flask, render_template, request, jsonify
import base64
import requests
import uuid

app = Flask(__name__)

API_URL = "https://internvl-eas-router.opengvlab.com/chat_with_internvl"


def encode_image(file):
    mime_type = file.mimetype
    image_data = file.read()
    ddcode = base64.b64encode(image_data).decode()
    base64_image = f"data:{mime_type};base64,{ddcode}"
    return base64_image, len(image_data)


@app.route('/')
def index():
    return render_template('form.html')


@app.route("/upload", methods=["POST"])
def upload():
    if "images" not in request.files or "question" not in request.form:
        return jsonify({"error": "Please upload at least one image and enter a question."}), 400

    images = request.files.getlist("images")
    question = request.form["question"]

    base64_images = []
    image_bytes = []

    for image in images:
        base64_image, size = encode_image(image)
        base64_images.append(base64_image)
        image_bytes.append({"bytes": size, "max_dynamic_patch": 12})

    content = [{"type": "text", "text": question}]

    for index, image in enumerate(base64_images):
        if image:
            content.append({
                "type": "image_url",
                "image_url": {"url": image, "max_dynamic_patch": 12},
                "image_bytes": image_bytes[index]
            })

    payload = {
        "model": "InternVL2.5-78B",
        "messages": [
            {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": content,
                "liked": ""
            }
        ],
        "stream": True,
        "language": "en-US",
        "prompt": "Please answer the user's question as detailed as possible.",
        "temperature": 0.7,
        "top_p": 0.95,
        "repetition_penalty": 1.1,
        "max_new_token": 1024,
        "max_input_tiles (control image resolution)": 12,
        "api": "/v1/chat/completions"
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload,
                             headers=headers, verify=False)

    if response.status_code != 200:
        return jsonify({"error": "Failed to communicate with API."}), 500

    output = ""
    for line in response.text.split("\n"):
        if line.startswith("data:"):
            try:
                data = json.loads(line[5:])
                if "choices" in data and len(data["choices"]) > 0 and "delta" in data["choices"][0] and "content" in data["choices"][0]["delta"]:
                    output += data["choices"][0]["delta"]["content"]
            except json.JSONDecodeError:
                continue

    return jsonify({"response": output})


if __name__ == "__main__":
    app.run(debug=True)
