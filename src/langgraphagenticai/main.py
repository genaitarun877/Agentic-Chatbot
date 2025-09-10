import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
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
    user_message=st.chat_input("Enter your message here:")
    
    if user_message:
        try:
        ## Configure LLM Model
           obj_llm_config=GroqLLM(user_controls_input=user_input)
           model=obj_llm_config.get_llm_model()

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
                 st.error(f"Error: Graph Setup Failed - {str(e)}")
                 return
            
        except Exception as e:
                st.error(f"Graph Setup Failed - {str(e)}")
                return
    