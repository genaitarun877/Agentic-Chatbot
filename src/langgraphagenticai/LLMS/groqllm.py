import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input['GROQ_API_KEY']
            selected_groq_model = self.user_controls_input['selected_model']
            
            # Check if API key is provided
            if groq_api_key == '' and os.environ.get('GROQ_API_KEY', '') == '': 
                st.error("🔑 Please enter your Groq API Key to use Groq models")
                return None
            
            # Use the provided API key or fall back to environment variable
            api_key = groq_api_key if groq_api_key else os.environ.get('GROQ_API_KEY')
            
            llm = ChatGroq(api_key=api_key, model=selected_groq_model)
            
        except Exception as e:
            error_message = str(e).lower()
            
            # Handle specific error cases with user-friendly messages
            if 'unauthorized' in error_message or 'invalid api key' in error_message:
                st.error("🚫 **Invalid Groq API Key!** \n\n"
                        "Please check your API key and try again. \n\n"
                        "💡 **Tip**: Make sure you're using a valid Groq API key, not OpenAI or Gemini.")
            elif 'model' in error_message and 'not found' in error_message:
                st.error(f"🤖 **Model '{selected_groq_model}' not found!** \n\n"
                        "Please select a different Groq model from the dropdown.")
            elif 'rate limit' in error_message or 'quota' in error_message:
                st.error("⏰ **Rate limit exceeded!** \n\n"
                        "You've reached your Groq API usage limit. Please wait or check your plan.")
            elif 'network' in error_message or 'connection' in error_message:
                st.error("🌐 **Network Error!** \n\n"
                        "Please check your internet connection and try again.")
            else:
                # Generic error message for unknown issues
                st.error(f"❌ **Groq API Error!** \n\n"
                        f"Something went wrong with Groq: {str(e)} \n\n"
                        f"💡 **Try**: Check your API key or select a different model.")
            return None
            
        return llm
