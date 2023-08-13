import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a Personalized Learning Companion. Feel free to ask questions or discuss subjects you need help with. The AI will provide explanations, examples, practice problems, and more to assist your learning.
"""

# @chatbot("personalized-learning-companion")
def on_message(message_history: List[Message], state: dict = None):
    if state is None:
        state = {"subject": None, "quiz_question": None, "quiz_answer": None}

    user_input = message_history[-1].content.lower()

    if "quiz_answer" in state:
        if user_input.strip() == state["quiz_answer"].strip():
            bot_response = "Correct! Well done."
            state["quiz_question"] = None
            state["quiz_answer"] = None
        else:
            bot_response = "Oops! That's not the correct answer. Try again."

    elif state["quiz_question"]:
        bot_response = state["quiz_question"]
        state["quiz_answer"] = user_input

    elif user_input.startswith("quiz"):
        state["quiz_question"] = "What's the capital of France?"
        bot_response = "Sure! Here's a quiz question for you: What's the capital of France?"

    elif user_input.startswith("study schedule"):
        bot_response = "Let's plan your study schedule. What subjects do you need to study? Please provide a comma-separated list."

    elif "subject" in state:
        bot_response = f"Great! Let's learn about {state['subject']}. I'll provide explanations and examples. Feel free to ask questions."

    else:
        bot_response = "Welcome to your Personalized Learning Companion. What subject do you need help with?"

    return bot_response, state

if __name__ == "__main__":
    print("Personalized Learning Companion")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break
        
        response, _ = on_message([Message("user", user_input)])
        print(f"Bot: {response}")
