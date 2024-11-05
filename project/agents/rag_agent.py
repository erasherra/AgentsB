from embedchain import App


class RAGAgent:
    def __init__(self, node, model_manager=None):
        self.id = node["id"]
        self.label = node["assigned"]["label"]
        self.custom_name = node["assigned"]["customName"]
        self.custom_type = node["assigned"]["customType"]
        self.custom_config = node["assigned"]["customConfig"]
        self.sources = node["assigned"]["customConfig"]["sources"]#[source["source"] for source in self.custom_config["sources"]]
        self.system_prompt = self.custom_config["system_prompt"]
        self.llm = model_manager.get_model(node["llm"]["selected"])

        self.embedchain_config = select_config()
        
            
        bot = App.from_config(config=self.embedchain_config)

        for item in self.sources:
            print("Adding: ", item["link"], item["type"])
            bot.add(item["source"], data_type=item["type"])

        self.bot = bot
        
    def process_input(self, input_data):
        # TO DO: implement RAG agent logic
        # For now, just return the input data as is
        #return input_data + " <start> " +  self.id + self.custom_type + " </end> "# output
        
        answer, sources = self.bot.query(query, citations=True)
        return answer
    
    def select_config(self):
        
        llm_config = None
        if self.llm.get_model_type() == "OLLAMA":
            llm_config = {
                "llm": {
                  "provider": "ollama",
                  "config": {
                    "model": self.llm.get_model(),
                    "top_p": 0.5,
                    "stream": false,
                    "prompt": "\n$context\n\n$query\n\n",
                    "system_prompt": self.system_prompt
                  }
                }
            }
        elif self.llm.get_model_type() == "GPT":
            llm_config = {
                "llm": {
                    "provider": "openai",
                    "config": {
                      "model": self.llm.get_model(),
                      "temperature": 0.5,
                      "max_tokens": 1000,
                      "top_p": 1,
                      "stream": false,
                      "prompt": "\n$context\n\n$query\n\n",
                      "system_prompt": self.system_prompt,
                      "api_key": self.llm.get_api_key()
                    }
                }
            }
            
        return llm_config

    #def query(self, query):
    #    answer, sources = self.bot.query(query, citations=True)
    #    #self.bot.reset()
    #    #print(sources)
    #    #print(answer)
    #    return answer
#
    #def chat(self, text):
    #    answer, sources = self.bot.chat(text, citations=True)
    #    self.bot.reset()
    #    self.bot.delete_session_chat_history()
    #    return answer