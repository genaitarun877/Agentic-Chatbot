import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            gemini_api_key = self.user_controls_input['GEMINI_API_KEY']
            selected_gemini_model = self.user_controls_input['selected_model']
            
            # Check if API key is provided
            if gemini_api_key == '' and os.environ.get('GOOGLE_API_KEY', '') == '':
                st.error("🔑 Please enter your Google/Gemini API Key to use Gemini models")
                return None
            
            # Use the provided API key or fall back to environment variable
            api_key = gemini_api_key if gemini_api_key else os.environ.get('GOOGLE_API_KEY')
            
            llm = ChatGoogleGenerativeAI(
                model=selected_gemini_model,
                google_api_key=api_key,
                temperature=0.7
            )
            
        except Exception as e:
            error_message = str(e).lower()
            
            # Handle specific error cases with user-friendly messages
            if 'invalid api key' in error_message or 'unauthorized' in error_message or 'forbidden' in error_message:
                st.error("🚫 **Invalid Google/Gemini API Key!** \n\n"
                        "Please check your API key and try again. \n\n"
                        "💡 **Tip**: Make sure you're using a valid Google AI API key, not OpenAI or Groq.")
            elif 'model' in error_message and ('not found' in error_message or 'not supported' in error_message):
                st.error(f"🤖 **Model '{selected_gemini_model}' not found!** \n\n"
                        "Please select a different Gemini model from the dropdown.")
            elif 'quota' in error_message or 'rate limit' in error_message:
                st.error("⏰ **Google AI Usage Limit Reached!** \n\n"
                        "You've exceeded your Gemini API quota or rate limit. \n\n"
                        "💳 Check your Google AI usage or wait before trying again.")
            elif 'network' in error_message or 'connection' in error_message:
                st.error("🌐 **Network Error!** \n\n"
                        "Please check your internet connection and try again.")
            elif 'billing' in error_message:
                st.error("💳 **Billing Issue!** \n\n"
                        "There seems to be an issue with your Google AI billing. \n\n"
                        "Please check your Google Cloud billing account.")
            else:
                # Generic error message for unknown issues
                st.error(f"❌ **Gemini API Error!** \n\n"
                        f"Something went wrong with Gemini: {str(e)} \n\n"
                        f"💡 **Try**: Check your API key or select a different model.")
            return None
            
        return llm
