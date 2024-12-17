class InputHandler:
    def __init__(self):
        self.id = "i"
        self.input = ""
        self.output = ""
        
    def set_input(self, input_data):
        self.input += f"""
        {input_data}

        """
        
    def process_input(self):
        print("InputHandler", self.input)
        self.output += self.input
        return self.output