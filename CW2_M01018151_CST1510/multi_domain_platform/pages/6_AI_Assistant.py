# gemini_chat.py
import streamlit as st
from google import genai
from google.genai import types


class GeminiChatAssistant:
    """Handles Gemini AI chat functionality."""

    def __init__(self):
        self.__username = st.session_state.get("username", "User")
        self.__user_role = st.session_state.get("user_role", "user")
        self.__client = None
        self.__api_key = None
        self.__model = "gemini-2.5-flash"
        self.__temperature = 0.7

    def __check_login(self) -> bool:
        """Check if user is logged in."""
        if not st.session_state.get("logged_in", False):
            st.error("🔒 You need to be logged in to access the AI Assistant")
            if st.button("Go to Login"):
                st.switch_page("OOP_home.py")
            st.stop()
        return True

    def __get_api_key(self) -> str:
        """Get API key from secrets or manual input."""
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✓ Using API key from secrets")
            return api_key
        except:
            api_key = None

        if not api_key:
            st.warning("No API key found in secrets")
            api_key_input = st.text_input(
                "Enter your Gemini API Key:",
                type="password",
                placeholder="Paste API key here...",
                key="api_key_input"
            )

            if api_key_input:
                api_key = api_key_input
                st.success("✓ Using entered API key")
            else:
                st.error("Please enter an API key")
                st.stop()

        return api_key

    def __setup_sidebar(self):
        """Setup sidebar configuration."""
        with st.sidebar:
            st.title("Gemini AI Assistant")
            st.subheader("Chat with an AI ASSISTANT")

            self.__api_key = self.__get_api_key()

            st.divider()

            # Model settings
            st.subheader("🤖 Model Settings")

            self.__model = st.selectbox(
                "Select Model:",
                ["gemini-2.5-flash"],
                index=0,
                help="Choose the AI model to use"
            )

            self.__temperature = st.slider(
                "Creativity (Temperature):",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make responses more creative, lower values more focused"
            )

            st.divider()

            # Chat controls
            st.subheader("💬 Chat Controls")

            if st.button("🗑 Clear Chat History", use_container_width=True, type="secondary"):
                if 'messages' in st.session_state:
                    st.session_state.messages = []
                    st.success("Chat cleared!")
                    st.rerun()

            st.divider()

            # User info
            st.subheader("👤 User Info")
            st.info(f"**Username:** {self.__username}\n\n**Role:** {self.__user_role}")

    def __initialize_client(self):
        """Initialize Gemini client."""
        if self.__api_key:
            try:
                self.__client = genai.Client(api_key=self.__api_key)
            except Exception as e:
                st.error(f"Failed to initialize client: {e}")
                st.stop()
        else:
            st.error("API key not set")
            st.stop()

    def __initialize_chat_history(self):
        """Initialize chat history with welcome message."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Welcome message if chat is empty
        if len(st.session_state.messages) == 0:
            welcome_message = f"Hello {self.__username}! I'm your AI assistant. I can help with analysis and explanations. What would you like to discuss today?"

            #  welcome message to session state
            if not any(msg["role"] == "model" and welcome_message in msg["parts"][0]["text"]
                       for msg in st.session_state.messages):
                st.session_state.messages.append({
                    "role": "model",
                    "parts": [{"text": welcome_message}]
                })

    def __display_messages(self):
        """Display existing chat messages."""
        for message in st.session_state.messages:
            if message["role"] == "model":
                role = "assistant"
                avatar = "🤖"
            else:
                role = "user"
                avatar = "👤"

            with st.chat_message(role, avatar=avatar):
                st.markdown(message["parts"][0]["text"])

    def __display_conversation_stats(self):
        """Display conversation statistics."""
        message_count = len(st.session_state.get("messages", []))
        user_messages = sum(1 for msg in st.session_state.messages if msg["role"] == "user")
        ai_messages = sum(1 for msg in st.session_state.messages if msg["role"] == "model")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", message_count)
        with col2:
            st.metric("Your Messages", user_messages)
        with col3:
            st.metric("AI Responses", ai_messages)

        st.markdown("---")

    def __get_system_prompt(self) -> str:
        """Get system prompt based on user role."""
        if self.__user_role == "admin":
            return f"You are an AI assistant for an admin user named {self.__username} at a Multi-Domain Intelligence Platform. Provide detailed, technical responses suitable for system administration and management."
        elif self.__user_role == "analyst":
            return f"You are an AI assistant for an analyst named {self.__username} at a Multi-Domain Intelligence Platform. Provide analytical, data-driven responses with insights and recommendations."
        else:
            return f"You are a helpful AI assistant for {self.__username} at a Multi-Domain Intelligence Platform. Provide clear, informative responses suitable for general users."

    def __process_user_input(self, prompt: str):
        """Process user input and get AI response."""
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        # Send to Gemini
        try:
            system_prompt = self.__get_system_prompt()

            response = self.__client.models.generate_content_stream(
                model=self.__model,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=self.__temperature
                ),
                contents=st.session_state.messages,
            )

            # Display streaming assistant output
            with st.chat_message("assistant", avatar="🤖"):
                container = st.empty()
                full_reply = ""
                for chunk in response:
                    full_reply += chunk.text
                    container.markdown(full_reply)

            # Save assistant message
            st.session_state.messages.append({"role": "model", "parts": [{"text": full_reply}]})

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Please check your API key and internet connection")

    def run(self):
        """Main method to run the chat assistant."""
        # Page configurations
        st.set_page_config(
            page_title="AI Assistant",
            page_icon="🤖",
            layout="wide"
        )

        # Check login
        self.__check_login()

        # Page header
        st.title(f"🤖 AI Assistant")
        st.markdown(f"Welcome back, **{self.__username}**! I'm your AI assistant. How can I help you today?")

        # Back button
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("← Dashboard"):
                st.switch_page("pages/2_Dashboard.py")

        st.markdown("---")

        # Setup sidebar
        self.__setup_sidebar()

        # Initialize client
        self.__initialize_client()

        # Initialize chat history
        self.__initialize_chat_history()

        # Display messages
        self.__display_messages()

        # Display conversation stats
        self.__display_conversation_stats()

        # User input
        prompt = st.chat_input(f"Type your message here, {self.__username}...")

        if prompt:
            self.__process_user_input(prompt)

        # Bottom navigation
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(" Return to Dashboard", use_container_width=True):
                st.switch_page("pages/2_Dashboard.py")


# Main execution
if __name__ == "__main__":
    assistant = GeminiChatAssistant()
    assistant.run()