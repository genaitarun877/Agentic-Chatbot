import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.Openaillm import OpenaiLLM
from src.langgraphagenticai.LLMS.geminillm import GeminiLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and run the LangGraph Agentic AI app With Streamlit UI.
    This function initializes the UI,Handles user input,configures the LLM model,
    sets up the graph based on the selelcted use case, displays the ouput while 
    implementing exception handling for robustness
    """

    ## Load ui
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Please enter a valid input")
        return
        
    # Store user controls in session state for news summarizer
    st.session_state['user_controls'] = user_input
    
    # For AI News Summarizer, check if button was clicked instead of waiting for chat input
    if user_input.get('selected_usecase') == "AI News Summarizer":
        if user_input.get('generate_news_summary', False):
            user_message = "Generate AI News Summary"  # Trigger the news summarization
        else:
            # Show instructions for the news summarizer
            st.info("📰 **AI News Summarizer Ready!** \n\n"
                   "1. Select your preferred time range (3, 6, or 10-15 days)\n"
                   "2. Click the '🚀 Generate AI News Summary' button\n"
                   "3. Wait for the latest AI/ML/Tech news summary")
            return
    else:
        user_message=st.chat_input("Enter your message here:")
    
    if user_message:
        try:
        ## Configure LLM Model based on selected LLM
           selected_llm = user_input.get('selected_llm', 'Groq')
           
           if selected_llm == 'Groq':
               obj_llm_config = GroqLLM(user_controls_input=user_input)
           elif selected_llm == 'OpenAI':
               obj_llm_config = OpenaiLLM(user_controls_input=user_input)
           elif selected_llm == 'Gemini':
               obj_llm_config = GeminiLLM(user_controls_input=user_input)
           else:
               st.error(f"Unsupported LLM: {selected_llm}")
               return
               
           model = obj_llm_config.get_llm_model()

           if not model:
               st.error("Error configuring LLM Model")
               return
            
        ## Initialize Graph based on the usecase
           usecase=user_input['selected_usecase']

           if not usecase:
               st.error("Please select a valid use case")
               return
           
           ## Graph builder

           graph_builder=GraphBuilder(model)

           try:
               graph=graph_builder.setup_graph(usecase)
               DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
           except Exception as e:
               # Handle cross-provider API key errors with user-friendly messages
               error_str = str(e).lower()
               
               # Detect OpenAI selected but wrong API key used
               if selected_llm == 'OpenAI':
                   if 'aizasy' in error_str or 'google' in error_str or 'gemini' in error_str:
                       st.error("😱 **Oops! Wrong API Key!** \n\n"
                               "You selected **OpenAI** but entered a **Google/Gemini API key** (starts with AIzaSy...). \n\n"
                               "🔄 **Fix**: Use your OpenAI API key (starts with sk-...) instead, or switch to Gemini provider.")
                   elif 'groq' in error_str or 'gsk_' in error_str:
                       st.error("😱 **Oops! Wrong API Key!** \n\n"
                               "You selected **OpenAI** but entered a **Groq API key** (starts with gsk_...). \n\n"
                               "🔄 **Fix**: Use your OpenAI API key (starts with sk-...) instead, or switch to Groq provider.")
                   elif 'incorrect api key' in error_str or 'invalid api key' in error_str:
                       st.error("🚫 **Invalid OpenAI API Key!** \n\n"
                               "Your OpenAI API key appears to be invalid or expired. \n\n"
                               "🔑 **Get a new key**: https://platform.openai.com/account/api-keys")
                   else:
                       st.error(f"❌ **OpenAI Error!** \n\n{str(e)}")
               
               # Detect Groq selected but wrong API key used
               elif selected_llm == 'Groq':
                   if 'openai' in error_str or 'sk-' in error_str:
                       st.error("😱 **Oops! Wrong API Key!** \n\n"
                               "You selected **Groq** but entered an **OpenAI API key** (starts with sk-...). \n\n"
                               "🔄 **Fix**: Use your Groq API key (starts with gsk_...) instead, or switch to OpenAI provider.")
                   elif 'aizasy' in error_str or 'google' in error_str or 'gemini' in error_str:
                       st.error("😱 **Oops! Wrong API Key!** \n\n"
                               "You selected **Groq** but entered a **Google/Gemini API key** (starts with AIzaSy...). \n\n"
                               "🔄 **Fix**: Use your Groq API key (starts with gsk_...) instead, or switch to Gemini provider.")
                   else:
                       st.error(f"❌ **Groq Error!** \n\n{str(e)}")
               
               # Detect Gemini selected but wrong API key used
               elif selected_llm == 'Gemini':
                   if 'openai' in error_str or 'sk-' in error_str:
                       st.error("😱 **Oops! Wrong API Key!** \n\n"
                               "You selected **Gemini** but entered an **OpenAI API key** (starts with sk-...). \n\n"
                               "🔄 **Fix**: Use your Google/Gemini API key (starts with AIzaSy...) instead, or switch to OpenAI provider.")
                   elif 'groq' in error_str or 'gsk_' in error_str:
                       st.error("😱 **Oops! Wrong API Key!** \n\n"
                               "You selected **Gemini** but entered a **Groq API key** (starts with gsk_...). \n\n"
                               "🔄 **Fix**: Use your Google/Gemini API key (starts with AIzaSy...) instead, or switch to Groq provider.")
                   else:
                       st.error(f"❌ **Gemini Error!** \n\n{str(e)}")
               
               else:
                   st.error(f"❌ **Error: Graph Setup Failed** \n\n{str(e)}")
               return
            
        except Exception as e:
            # Handle cross-provider API key errors at the main level too
            error_str = str(e).lower()
            selected_llm = user_input.get('selected_llm', 'Unknown')
            
            # Check for cross-provider API key issues
            if selected_llm == 'OpenAI' and ('aizasy' in error_str or 'google' in error_str):
                st.error("😱 **Wrong API Key Detected!** \n\n"
                        "You selected **OpenAI** but provided a **Google/Gemini API key**. \n\n"
                        "🔄 **Solution**: Either use your OpenAI API key or switch to Gemini provider.")
            elif selected_llm == 'Groq' and ('aizasy' in error_str or 'openai' in error_str):
                st.error("😱 **Wrong API Key Detected!** \n\n"
                        "You selected **Groq** but provided the wrong API key. \n\n"
                        "🔄 **Solution**: Use your Groq API key or switch providers.")
            elif selected_llm == 'Gemini' and ('openai' in error_str or 'groq' in error_str):
                st.error("😱 **Wrong API Key Detected!** \n\n"
                        "You selected **Gemini** but provided the wrong API key. \n\n"
                        "🔄 **Solution**: Use your Google/Gemini API key or switch providers.")
            elif 'incorrect api key' in error_str or 'invalid api key' in error_str:
                st.error(f"🚫 **Invalid API Key!** \n\n"
                        f"The {selected_llm} API key you provided is invalid. \n\n"
                        f"🔑 Please check your API key and try again.")
            else:
                st.error(f"❌ **Application Error!** \n\n{str(e)}")
            return
    