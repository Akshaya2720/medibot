import gradio as gr
import google.generativeai as genai

# Step 1: Configure the Gemini API with your API key
API_KEY = "AIzaSyCxNnxkmOQnkiCs0MoDVOgwuwXW2qQuChA"  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

# Step 2: Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')  # Use 'gemini-pro' for text-only interactions

# Rule-based responses
responses = {
    "hi": "**Hello!** Please describe your symptoms so I can help you.",
    "hello": "**Hi there!** Could you tell me what symptoms you're experiencing?",
    "how are you": "I'm just a bot, but I'm here to help! What symptoms are you feeling?",
    "bye": "**Goodbye!** Take care and feel better soon!",
}

# Custom CSS for styling
css = """
body {
    background-color: #1E90FF; /* Royal Green (light green) */
    font-family: 'Poppins', sans-serif;
    color: #fff; /* White text for contrast */
    margin: 0;
    padding: 0;
}
.gr-button {
    background-color: #4CAF50; /* Green button */
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
}
.gr-textbox {
    border: 2px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
    background-color: #fff; /* White background for input fields */
    color: #333; /* Dark text for input fields */
}
.gr-slider {
    width: 100%;
    margin-top: 10px;
}
.gr-output {
    background-color: #fff; /* White background for output */
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    font-size: 16px;
    margin-top: 20px;
    min-height: 100px;
    color: #333; /* Dark text for output */
}
"""

# Step 3: Define the chatbot function
conversation_history = []  # Store conversation history

def chatbot_response(user_input):
    global conversation_history
    
    # Check if the user input matches a known question in the rule-based system
    user_input = user_input.lower()
    
    # Rule-based response
    if user_input in responses:
        return responses[user_input]
    
    # Add user input to conversation history
    conversation_history.append(f"User: {user_input}")
    
    # Generate response from Gemini
    try:
        # Combine conversation history into a single prompt
        full_conversation = "\n".join(conversation_history)
        prompt = f"Conversation history:\n{full_conversation}\n\nBased on the above conversation, respond appropriately."
        response = model.generate_content(prompt)
        
        # Add bot response to conversation history
        bot_response = response.text
        conversation_history.append(f"Bot: {bot_response}")
        
        return bot_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Step 4: Create the Gradio Interface
with gr.Blocks(css=css, title="🌟 **Interactive Symptom-Based Disease Detection Chatbot** 🌟") as demo:
    # Bold and creative headings
    gr.Markdown("# 🩺 **Interactive Symptom-Based Disease Detection Chatbot**")
    gr.Markdown("**Describe your symptoms or ask questions. The chatbot will remember your conversation history!**")

    # Chat interface
    chatbot = gr.Chatbot(label="Chat History", height=300)  # Displays the conversation history
    user_input = gr.Textbox(label="Your Message", placeholder="Type your message here...")
    submit_button = gr.Button("Send")
    clear_button = gr.Button("Clear Chat")

    # Function to handle user input and update chat history
    def respond(message, chat_history):
        bot_response = chatbot_response(message)
        chat_history.append((message, bot_response))  # Update chat history
        return "", chat_history  # Clear input box and return updated chat history

    # Bind buttons to functions
    submit_button.click(respond, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    clear_button.click(lambda: ([], []), outputs=[chatbot, user_input])  # Clear chat history and input box

# Step 5: Launch the Gradio app
demo.launch(share=True)