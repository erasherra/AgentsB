class OutputHandler:
    def __init__(self):
        self.id = "o"
        self.input = ""
        self.output = ""
        
    def set_input(self, input_data):
        self.input += f"""
        {input_data}

        """
        
    def process_input(self):
        print("OutputHandler", self.input)
        self.output += self.input
        return self.output