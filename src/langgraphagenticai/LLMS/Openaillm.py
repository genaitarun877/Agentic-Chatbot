import os
import streamlit as st
from langchain_openai import ChatOpenAI

class OpenaiLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input

    def get_llm_model(self):
        try:
            openai_api_key = self.user_controls_input['OPENAI_API_KEY']
            selected_openai_model = self.user_controls_input['selected_model']
            
            # Check if API key is provided
            if openai_api_key == '' and os.environ.get('OPENAI_API_KEY', '') == '':  
                st.error("🔑 Please enter your OpenAI API Key to use OpenAI models")
                return None
            
            # Use the provided API key or fall back to environment variable
            api_key = openai_api_key if openai_api_key else os.environ.get('OPENAI_API_KEY')
            
            llm = ChatOpenAI(api_key=api_key, model=selected_openai_model)
            
        except Exception as e:
            error_message = str(e).lower()
            
            # Handle specific error cases with user-friendly messages
            if 'unauthorized' in error_message or 'invalid api key' in error_message or 'incorrect api key' in error_message:
                st.error("🚫 **Invalid OpenAI API Key!** \n\n"
                        "Please check your API key and try again. \n\n"
                        "💡 **Tip**: Make sure you're using a valid OpenAI API key, not Groq or Gemini.")
            elif 'model' in error_message and ('not found' in error_message or 'does not exist' in error_message):
                st.error(f"🤖 **Model '{selected_openai_model}' not found!** \n\n"
                        "Please select a different OpenAI model from the dropdown.")
            elif 'rate limit' in error_message or 'quota' in error_message or 'billing' in error_message:
                st.error("⏰ **OpenAI Usage Limit Reached!** \n\n"
                        "You've exceeded your OpenAI API quota or rate limit. \n\n"
                        "💳 Check your OpenAI billing or wait before trying again.")
            elif 'network' in error_message or 'connection' in error_message:
                st.error("🌐 **Network Error!** \n\n"
                        "Please check your internet connection and try again.")
            else:
                # Generic error message for unknown issues
                st.error(f"❌ **OpenAI API Error!** \n\n"
                        f"Something went wrong with OpenAI: {str(e)} \n\n"
                        f"💡 **Try**: Check your API key or select a different model.")
            return None
            
        return llm
