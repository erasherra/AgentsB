from embedchain import App


class RAGAgent:
    def __init__(self, node, model_manager=None, stream=False):
        self.id = node["id"]
        self.label = node["assigned"]["label"]
        self.custom_name = node["assigned"]["customName"]
        self.custom_type = node["assigned"]["customType"]
        self.custom_config = node["assigned"]["customConfig"]
        self.sources = node["assigned"]["customConfig"]["sources"]#[source["source"] for source in self.custom_config["sources"]]
        self.system_prompt = self.custom_config["system_prompt"]
        self.llm = model_manager.get_model(node["llm"]["selected"])


        self.embedchain_config = model_manager.select_rag_config(self.llm.get_model_type(), self.llm.get_model(), self.system_prompt, self.llm.get_api_key(), stream)
        
        print("asd " , self.embedchain_config)    
        bot = App.from_config(config=self.embedchain_config)

        for item in self.sources:
            print("Adding: ", item["source"], item["type"])
            bot.add(item["source"], data_type=item["type"])

        self.bot = bot
        
   
    def process(self, input_data):
        
        answer, sources = self.bot.query(input_data, citations=True)
        if answer is not None:
            response = f"""
            #{self.label}:

            {answer}
            """
            return response
        
        return ""
    
    async def process_stream(self, input_data, websocket=None):
        
        if websocket:

            answer = ""
            header = f"""
            {self.label}:

            """
            await websocket.send_text(header)
            for chunk in self.bot.query(input_data, citations=False):
                print(chunk, end="|", flush=True)
                await websocket.send_text(chunk)
                answer += chunk

            await websocket.send_text("$$END$$")
            if answer is not None:
                response = f"""
                #{self.label}:

                {answer}
                """
                return response
        
        return ""
    
    def process_input(self, input_data):
        # TO DO: implement RAG agent logic
        # For now, just return the input data as is
        #return input_data + " <start> " +  self.id + self.custom_type + " </end> "# output
        
        
        return self.process(input_data)
    