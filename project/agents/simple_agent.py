class LLMAgent:
    def __init__(self, node, model_manager=None):
        self.id = node["id"]
        self.label = node["assigned"]["label"]
        self.custom_name = node["assigned"]["customName"]
        self.custom_type = node["assigned"]["customType"]
        self.custom_config = node["assigned"]["customConfig"]
        self.system_prompt = self.custom_config["system_prompt"]
        self.llm = model_manager.get_model(node["llm"]["selected"])

        
    
    def process(self, input_data):
        answer = self.llm.send(input_data, self.system_prompt)

        response = f"""
        **{self.label}:**

        {answer}
        """
        return response
        
    
    async def process_stream(self, input_data, websocket=None):
        
        if websocket:
            return await self.llm.stream(self.label, input_data, self.system_prompt, websocket)
        
        return "stream"
        
    def process_input(self, input_data):
        # TO DO: implement LLM agent logic
        # For now, just return the input data as is
        #return input_data + " <start> " +  self.id + self.custom_type + " </end> "# output
        
        
        return self.process(input_data)
        
    
    