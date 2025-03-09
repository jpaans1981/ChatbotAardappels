import streamlit as st
import openai

# Set your OpenAI API key
# In production, use st.secrets["OPENAI_API_KEY"] instead of hardcoding
openai.api_key = "your-api-key-here"  # Replace with your actual API key for testing

# App title and description
st.title("My AI Chatbot")
st.subheader("Ask me anything!")
st.write("This is a simple AI chatbot built with Streamlit and OpenAI's API.")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate response from OpenAI
def generate_response(prompt):
    try:
        # Include conversation history for context
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        response = generate_response(prompt)
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with instructions
with st.sidebar:
    st.header("About")
    st.write("This chatbot uses OpenAI's GPT-3.5 Turbo model to generate responses.")
    
    st.header("Instructions")
    st.write("1. Type your question in the input box at the bottom")
    st.write("2. Press Enter to send your message")
    st.write("3. The AI will generate a response")
    
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()