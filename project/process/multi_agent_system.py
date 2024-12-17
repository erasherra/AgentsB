from project.llms.model_manager import ModelManager
from project.agents.simple_agent import LLMAgent
from project.agents.rag_agent import RAGAgent
from project.agents.input_handler import InputHandler
from project.agents.output_handler import OutputHandler
import json

class MultiAgentSystem:
    def __init__(self, agent_setup=None, model_manager=None):
        """
        Initializes the multi-agent system by reading the setup data from the
        provided JSON file and instantiating the agents.

        :param agent_setup: The path to the JSON file containing the agent
                             setup. Default is "process.json"
        """
        self.setup = agent_setup
        if model_manager is None:
            model_manager = ModelManager()

        self.agents = []
        for node in self.setup["nodes"]:
            
            if node["id"] == "i":
                agent = InputHandler()
            elif node["id"] == "o":
                agent = OutputHandler()
            elif node["assigned"]["customType"] == "AGENT":
                agent = LLMAgent(node, model_manager)
            elif node["assigned"]["customType"] == "RAG":
                agent = RAGAgent(node, model_manager)
            else:
                raise ValueError(f"Unsupported custom type: {node['customType']}")
            self.agents.append(agent)

        self.model_manager = model_manager

    def process_input(self, input_data):

        nodes = self.setup["nodes"]
        edges = self.setup["edges"]

        memory = ""
        self.update_agent("i", input_data)
        # Check if the node_queue queue is empty and if it is empty then go through self.agents and run agent process_input
        if not edges:
            for agent in self.agents:
                temp_input = agent.process_input(input_data)
                memory += f""" 
                
                {temp_input} 
                
                """
            return input_data, memory

        for edge in edges:
            
            agent = self.get_agent(edge["source"]) #next(a for a in self.agents if a.id == edge["source"]) # HERE is the PROBLEM
            output = agent.process_input()
            
            memory += output
            
            for target in edge["target"]:
                self.update_agent(target, output)
     
        for i, agent in enumerate(self.agents):
            if agent.id == "o":
                final_output = agent.input
                
            self.agents[i].output = ""
            self.agents[i].input = "" 
             
        final_memory = memory
        memory = ""    
        #agent_output = next(a for a in self.agents if a.id == "o")
        #final_output = agent_output.input
        #########  
        return final_output, final_memory

    def update_agent(self, target, output):
        for i, agent in enumerate(self.agents):
            if agent.id == target:
                new_input = agent.input + f"""
                {output}
                        
                """
                setattr(agent, 'input', new_input)  # Update the value

                self.agents[i] = agent
                
    def get_agent(self, target_id):
        #print("get_agent", target_id)
        for agent in self.agents:
            if agent.id == target_id:
                return agent