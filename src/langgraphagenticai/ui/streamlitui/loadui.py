import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_control={}
    def load_streamlit_ui(self):
        title=self.config.get_page_title()
        st.set_page_config(page_title=f"🚀{title}",layout='wide')
        st.header(f"🚀{title}")
    
        with st.sidebar:
           llm_options=self.config.get_llm_options()
           usecase_options=self.config.get_usecase_options()
           
           ##LLM selection
           self.user_control['selected_llm']=st.selectbox("Select LLM",llm_options)

           if self.user_control['selected_llm']=='Groq':
               ## model selection
               model_options=self.config.get_groq_model_options()
               self.user_control['selected_model']=st.selectbox("Select Model",model_options)
               ## API KEY
               self.user_control["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input('API Key',type="password")
               ## Validate API key
               if not self.user_control["GROQ_API_KEY"]:
                   st.warning("Please enter your Groq API Key")


           if self.user_control['selected_llm']=='OpenAI':
               ## model selection
               model_options=self.config.get_openai_model_options()
               self.user_control['selected_model']=st.selectbox("Select Model",model_options)
               ## API KEY
               self.user_control["OPENAI_API_KEY"]=st.session_state["OPENAI_API_KEY"]=st.text_input('API Key',type="password")
               ## Validate API key
               if not self.user_control["OPENAI_API_KEY"]:
                   st.warning("Please enter your OpenAI API Key")

           if self.user_control['selected_llm']=='Gemini':
               ## model selection
               model_options=self.config.get_gemini_model_options()
               self.user_control['selected_model']=st.selectbox("Select Model",model_options)
               ## API KEY
               self.user_control["GEMINI_API_KEY"]=st.session_state["GEMINI_API_KEY"]=st.text_input('Google/Gemini API Key',type="password")
               ## Validate API key
               if not self.user_control["GEMINI_API_KEY"]:
                   st.warning("Please enter your Google/Gemini API Key")
            ## Usecase selection
           self.user_control['selected_usecase']=st.selectbox("Select Use Case",usecase_options)

           if self.user_control['selected_usecase'] == "Chatbot with Web":
               os.environ["TAVILY_API_KEY"]=self.user_control["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input('TAVILY_API_KEY',type="password")

               if not self.user_control["TAVILY_API_KEY"]:
                   st.warning("Please enter your Tavily API Key")

           if self.user_control['selected_usecase'] == "AI News Summarizer":
               os.environ["TAVILY_API_KEY"]=self.user_control["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input('TAVILY_API_KEY',type="password")

               if not self.user_control["TAVILY_API_KEY"]:
                   st.warning("Please enter your Tavily API Key")
               
               # News summarizer specific controls
               st.subheader("📰 News Summary Settings")
               
               # Days selection dropdown
               days_options = ["3 days", "6 days", "10-15 days"]
               self.user_control['selected_days'] = st.selectbox(
                   "Select Days", 
                   days_options,
                   help="Choose the time range for news articles"
               )
               
               # Generate summary button
               self.user_control['generate_news_summary'] = st.button(
                   "🚀 Generate AI News Summary",
                   help="Click to generate AI/ML/Tech news summary for the selected time period",
                   use_container_width=True
               )
            
            
            
                   
    
        return self.user_control

           
               
