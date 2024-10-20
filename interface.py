import gradio as gr
from chatbot import process_query  # Assuming chatbot.py exists and contains the chatbot logic

# Gradio Interface to interact with the chatbot
def chatbot_interface(user_input):
    return process_query(user_input)

# Create the Gradio Interface
iface = gr.Interface(
    fn=chatbot_interface,
    inputs="text",
    outputs="json",  # Assuming JSON response from process_query
    title="Employee Database Chatbot",
    description="Ask questions about the employee database and get instant responses!"
)

# Launch the Gradio interface
if __name__ == "__main__":
    iface.launch(share=True)