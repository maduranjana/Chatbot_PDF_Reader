from transformers import pipeline

# Load the model
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

# Function to generate answer
def generate_answer(context, question):
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    result = qa_pipeline(prompt, max_length=200)
    return result[0]['generated_text']
