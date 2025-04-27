import requests

# Set your HuggingFace Inference API URL
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

# Your HuggingFace token
headers = {"Authorization": "Bearer ......"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_answer(context, question):
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    output = query({"inputs": prompt})
    
    try:
        return output[0]["generated_text"]
    except Exception as e:
        return "Sorry, I couldn't generate an answer."
