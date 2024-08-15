import gradio as gr
import requests
import numpy as np
import io
import soundfile as sf
import os 

# Backend API URL
API_URL = "http://127.0.0.1:5000"

def login(email):
    response = requests.post(f"{API_URL}/auth/login", json={"email": email})
    if response.status_code == 200:
        return "Login successful. Please proceed to the interview."
    else:
        return "Login failed. Please try again."

def get_question():
    response = requests.get(f"{API_URL}/questions")
    if response.status_code == 200:
        questions = response.json()
        if questions:
            return questions[0]['text']  # Return the first question
    return "No questions available."

def submit_answer(audio):
    # Define the path to save the audio file
    audio_file_path = "../recordings/recorded_audio.wav"
    
    # Convert numpy array to a WAV file and save it
    sf.write(audio_file_path, audio[1], samplerate=audio[0])
    
    # Send the saved WAV file to the backend
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio': (audio_file_path, audio_file)}
        data = {'question_id': '1'}  # Assuming question ID is 1 for simplicity
        
        response = requests.post(f"{API_URL}/answer", files=files, data=data)
    
    # Clean up the file after sending
    #os.remove(audio_file_path)
    
    if response.status_code == 200:
        result = response.json()
        return f"Score: {result['score']}/10\nFeedback: {result['feedback']}"
    else:
        return "Failed to submit answer. Please try again."

def generate_report():
    response = requests.get(f"{API_URL}/report")
    if response.status_code == 200:
        report = response.json()
        report_text = f"Overall Score: {report['overall_score']}/10\n\n"
        for answer in report['answers']:
            report_text += f"Question: {answer['question']}\n"
            report_text += f"Score: {answer['score']}/10\n"
            report_text += f"Feedback: {answer['feedback']}\n\n"
        return report_text
    else:
        return "Failed to generate report. Please try again."

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# AI-Powered Mock Interview")
    
    with gr.Tab("Login"):
        email_input = gr.Textbox(label="Enter your email")
        login_button = gr.Button("Login")
        login_output = gr.Textbox(label="Login Status")
        login_button.click(login, inputs=email_input, outputs=login_output)
    
    with gr.Tab("Interview") as interview_tab:
        question_box = gr.Textbox(label="Question")
        audio_input = gr.Audio(sources="microphone", type="numpy")
        submit_button = gr.Button("Submit Answer")
        result_box = gr.Textbox(label="Result")
        
        submit_button.click(submit_answer, inputs=audio_input, outputs=result_box)
        
        interview_tab.select(fn=get_question, outputs=question_box)
    
    with gr.Tab("Report"):
        generate_button = gr.Button("Generate Report")
        report_box = gr.Textbox(label="Interview Report")
        generate_button.click(generate_report, inputs=None, outputs=report_box)

demo.launch()
