

class ModelManager:
    def __init__(self):
        self.models = {}

    def add_model(self, model_type, model_instance):
        self.models[model_type] = model_instance

    def get_model(self, model_type):
        return self.models.get(model_type)

    def select_rag_config(self, model_type, model, system_prompt, api_key=None, stream=False):
        
        llm_config = None
        if model_type == "OLLAMA":
            llm_config = {
                "llm": {
                  "provider": "ollama",
                  "config": {
                    "model": model,
                    "top_p": 0.5,
                    "stream": stream,
                    "prompt": "\n$context\n\n$query\n\n",
                    "system_prompt": system_prompt
                  }
                }
            }
        elif model_type == "GPT":
            llm_config = {
                "llm": {
                    "provider": "openai",
                    "config": {
                      "model": model,
                      "temperature": 0.5,
                      "max_tokens": 1000,
                      "top_p": 1,
                      "stream": stream,
                      "prompt": "\n$context\n\n$query\n\n",
                      "system_prompt": system_prompt,
                      "api_key": api_key
                    }
                }
            }
            
        return llm_config  # output