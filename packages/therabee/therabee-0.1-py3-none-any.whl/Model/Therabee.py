import openai
key = "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"

# Set up your API key
openai.api_key = key

# System message to guide Therabee
system_message = {
    "role": "system",
    "content": ("You are a compassionate, qualified therapist who is allowed and expected to provide advice and emotional support. "
                "When the user expresses sadness or emotional distress, you are to respond with empathy and offer practical therapeutic advice. "
                "You are not only capable of discussing these feelings, but it is also your responsibility to help the user navigate their emotions. "
                "Always aim to provide actionable, helpful, and non-judgmental guidance in a way that promotes healing and understanding.")
}
# User's message
user_message = input("What's on your mind today? ")

# Create the conversation including the system message and the user message
conversation = [
    system_message,
    {"role": "user", "content": user_message}
]

# Send the conversation to the API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    max_tokens=200
)

# Extract and print the AI's response
reply = response['choices'][0]['message']['content']
print(reply)