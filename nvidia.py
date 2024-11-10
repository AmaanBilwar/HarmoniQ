from dotenv import load_dotenv
import requests, base64
import os


def analyze_image(image_path):
    load_dotenv()
    api_key = os.getenv("NVIDIA_NIM_API_KEY_2")

    invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
    stream = True

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    assert (
        len(image_b64) < 180_000
    ), "To upload larger images, use the assets API (see docs)"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "text/event-stream" if stream else "application/json",
    }

    payload = {
        "model": "meta/llama-3.2-90b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": f'Explain in brief how the person feels using the image. <img src="data:image/png;base64,{image_b64}" />',
            }
        ],
        "max_tokens": 512,
        "temperature": 1.00,
        "top_p": 1.00,
        "stream": stream,
    }

    response = requests.post(invoke_url, headers=headers, json=payload)

    if stream:
        final_message = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if data.startswith("data: "):
                    content = data[6:]
                    if content != "[DONE]":
                        # Extract the content from the JSON response
                        import json

                        json_data = json.loads(content)
                        if "choices" in json_data and len(json_data["choices"]) > 0:
                            delta = json_data["choices"][0].get("delta", {})
                            final_message += delta.get("content", "")
        if final_message:
            return final_message.strip()
        else:
            return "No result"
    else:
        json_response = response.json()
        if "choices" in json_response and len(json_response["choices"]) > 0:
            return json_response["choices"][0]["text"].strip()
        else:
            return "No result"
