import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class GPT:
    def __init__(self, api_key="empty", model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model

    def send(self, 
             prompt, 
             system_prompt="""Let's think step by step. 
             
             Question: """):
        
        if not self.api_key:
            raise ValueError("No API key provided")

        #TODO: Think some option to inject the question to location to system prompt
        template = system_prompt + """
        
        {question}
        
        """
        
        prompt_template = ChatPromptTemplate.from_template(template)
        model = ChatOpenAI(
            model=self.model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=self.api_key,
            # base_url="...",
            # organization="...",
            # other params...
            )
        chain = prompt_template | model
        response = chain.invoke({"question": prompt})
        
        if response is not None and response.content is not None:
            return response.content
        
        return ""
    
    async def stream(self, 
             prompt, 
             system_prompt="""Let's think step by step. 
             
             Question: """,
             websocket=None):
        
        if not self.api_key:
            raise ValueError("No API key provided")

        #TODO: Think some option to inject the question to location to system prompt
        template = system_prompt + """
        
        {question}
        
        """
        
        prompt_template = ChatPromptTemplate.from_template(template)
        model = ChatOpenAI(
            model=self.model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=self.api_key,
            # base_url="...",
            # organization="...",
            # other params...
            )
        chain = prompt_template | model
        
        response = ""
        for chunk in chain.stream({"question": prompt}):
            print(chunk.content, end="|", flush=True)
            await websocket.send_text(chunk.content)
            response += chunk.content
            
        if response is not None:
            return response
        
        return ""
    
    def get_api_key(self):
        return self.api_key
    
    def get_model(self):
        return self.model
    
    def get_model_type(self):
        return "GPT"