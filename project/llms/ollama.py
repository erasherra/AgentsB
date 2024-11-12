from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class Ollama:
    def __init__(self, api_key="empty", model="llama3:8b-instruct-q4_0"):
        if not api_key:
            api_key="empty"
        self.api_key = api_key  # Replace this with your actual API key
        self.model = model

    def send(self, 
             prompt, 
             system_prompt="""Let's think step by step. 
             
             Question: """):
        
        if not self.api_key:
            raise ValueError("No API key provided")

        #TODO: Think some option to inject the question to location to system prompt
        template = system_prompt + """{question}"""
        
        prompt_template = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model=self.model)
        chain = prompt_template | model
        response = chain.invoke({"question": prompt})
        
        print(response)
        print(type(response))
        if response is not None:
            return response
        
        return ""
    
    def get_api_key(self):
        return self.api_key
    
    def get_model(self):
        return self.model
    
    def get_model_type(self):
        return "OLLAMA"