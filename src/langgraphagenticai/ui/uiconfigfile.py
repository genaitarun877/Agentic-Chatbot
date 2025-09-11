from configparser import ConfigParser

class Config:
    def __init__(self,config_file='./src/langgraphagenticai/ui/uiconfigfile.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)
        
    def get_llm_options(self):
        llm_options = self.config["DEFAULT"].get("LLM_OPTIONS")
        return [opt.strip() for opt in llm_options.split(",")] if llm_options else []

    def get_usecase_options(self):
      usecase_options = self.config["DEFAULT"].get("USECASE_OPTIONS")
      return [opt.strip() for opt in usecase_options.split(",")] if usecase_options else []

    def get_groq_model_options(self):
       model_options = self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS")
       return [opt.strip() for opt in model_options.split(",")] if model_options else []
    
    def get_openai_model_options(self):
       model_options = self.config["DEFAULT"].get("OPENAI_MODEL_OPTIONS")
       return [opt.strip() for opt in model_options.split(",")] if model_options else []
    
    def get_gemini_model_options(self):
       model_options = self.config["DEFAULT"].get("GEMINI_MODEL_OPTIONS")
       return [opt.strip() for opt in model_options.split(",")] if model_options else []

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
    
    
