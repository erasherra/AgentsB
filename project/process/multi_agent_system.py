from project.llms.model_manager import ModelManager
from project.agents.simple_agent import LLMAgent
from project.agents.rag_agent import RAGAgent
import json
"""
Represents a multi-agent system. This class is responsible for initializing
the agents and processing input data.

Attributes:
- setup (dict): The initial setup of the agents, read from the JSON file.
- agents (list): A list of agent instances, one for each node in the graph.
"""

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

        #TODO
        debug_mode = False

        stream_switch = False
        
        self.agents = []
        for node in self.setup["nodes"]:
            if node["assigned"]["customType"] == "AGENT":
                agent = LLMAgent(node, model_manager)
            elif node["assigned"]["customType"] == "RAG":
                agent = RAGAgent(node, model_manager, stream_switch)
            else:
                raise ValueError(f"Unsupported custom type: {node['customType']}")
            self.agents.append(agent)

        self.model_manager = model_manager
    # Process the input data by visiting each node, processing it with its assigned agent,
    # and then exploring the connected agents. This function helps to simulate the behavior
    # of the multi-agent system.
    def process_input(self, input_data):
        # Initialize a set to keep track of visited nodes and an empty queue for nodes to be processed
        visited = set()
        node_queue = [(edge["source"], [next(n for n in self.setup["nodes"] if n["id"] == edge["source"])])
                   for edge in self.setup["edges"]]
        ## TODO: delete memory
        memory = input_data
        print("Input: ", memory)
        
        # Check if the node_queue queue is empty and if it is empty then go through self.agents and run agent process_input
        if not node_queue:
            for agent in self.agents:
                temp_input = agent.process_input(input_data)
                memory += f""" 
                
                {temp_input} 
                
                """
            return input_data, memory
        
        while node_queue:
            # Dequeue a node and its path, check if it has been visited before
            node_id, path = node_queue.pop(0)
            if node_id not in visited:
                visited.add(node_id)

                # Get the agent assigned to this node and process the input data with it
                agent = next(a for a in self.agents if a.id == node_id)
                input_data = agent.process_input(memory)
                input_data = f""" 
                
                {input_data} 
                
                """
                print("New Input: ", input_data)
                memory += input_data
                # Find all connected agents of this node that haven't been visited yet
                connected_agents = self.get_connected_agents(node_id)
                for target_node_id in connected_agents:
                    if target_node_id not in visited:
                        # For each connected agent, find the edges that connect it to other nodes,
                        # and add them to the queue for further processing
                        for edge in self.setup["edges"]:
                            if edge["source"] == node_id and target_node_id in edge["target"]:
                                node_queue.append((edge["target"][0], path + [next(n for n in self.setup["nodes"] if n["id"] == edge["target"][0])]))

        return input_data, memory

    # Streaming
    # TODO fuse this function with process_input
    async def process_input_stream(self, input_data, websocket):
        # Initialize a set to keep track of visited nodes and an empty queue for nodes to be processed
        visited = set()
        node_queue = [(edge["source"], [next(n for n in self.setup["nodes"] if n["id"] == edge["source"])])
                   for edge in self.setup["edges"]]
        ## TODO: delete memory
        memory = input_data
        print("Input: ", memory)
        
        # Check if the node_queue queue is empty and if it is empty then go through self.agents and run agent process_input
        if not node_queue:
            for agent in self.agents:
                temp_input = await agent.process_stream(input_data, websocket)
                memory += f""" 
                
                {temp_input} 
                
                """
            return input_data, memory
        
        while node_queue:
            # Dequeue a node and its path, check if it has been visited before
            node_id, path = node_queue.pop(0)
            if node_id not in visited:
                visited.add(node_id)

                # Get the agent assigned to this node and process the input data with it
                agent = next(a for a in self.agents if a.id == node_id)
                input_data = await agent.process_stream(memory, websocket)
                input_data = f""" 
                
                {input_data} 
                
                """
                print("New Input: ", input_data)
                memory += input_data
                # Find all connected agents of this node that haven't been visited yet
                connected_agents = self.get_connected_agents(node_id)
                for target_node_id in connected_agents:
                    if target_node_id not in visited:
                        # For each connected agent, find the edges that connect it to other nodes,
                        # and add them to the queue for further processing
                        for edge in self.setup["edges"]:
                            if edge["source"] == node_id and target_node_id in edge["target"]:
                                node_queue.append((edge["target"][0], path + [next(n for n in self.setup["nodes"] if n["id"] == edge["target"][0])]))

        return input_data, memory        

    # This method returns a list of node IDs that are directly connected to the given node.
    # It iterates over all edges in the system and checks if the given node is either
    # the source or target of an edge. If it's the source, it adds the targets of that edge
    # to the set of connected nodes; if it's a target, it adds the source of that edge.
    # Finally, it removes the given node from the set and returns the list of remaining nodes.
    def get_connected_agents(self, node_id):
        connected_agents = set()
        for edge in self.setup["edges"]:
            if edge["source"] == node_id:
                connected_agents.update(edge["target"])
            elif node_id in edge["target"]:
                connected_agents.add(edge["source"])
        return list(connected_agents - {node_id})

    def modify_agent(self, node_id, node):
        """
        Modifies an existing agent based on its ID.

        :param node_id: The ID of the node whose agent should be modified.
        """
        for agent in self.agents:
            if agent.id == node_id:
                # You can now modify the agent's properties here
                # For example, you could change its LLM or custom config
                print(f"Modifying agent at {node_id}...")
                if node["assigned"]["customType"] == "AGENT":
                    agent = LLMAgent(node, self.model_manager)
                elif node["assigned"]["customType"] == "RAG":
                    agent = RAGAgent(node, self.model_manager)
                else:
                    raise ValueError(f"Unsupported custom type: {node['customType']}")
                return
        print(f"No agent found with ID {node_id}.")

    def process_input_with_flexible_structure(self, input_data):
        # Step 1: Initialize memory and dependency tracking
        memory = {}
        in_degree = {node["id"]: 0 for node in self.setup["nodes"]}  # Track dependencies

        # Step 1.5: Check if edges are empty
        if not self.setup["edges"]:
            accumulated_output = ""  # Initialize an empty string to accumulate results

            # Step 2: Iterate over all nodes
            for node in self.setup["nodes"]:
                # Step 3: Find the corresponding agent
                agent = next(agent for agent in self.agents if agent.id == node["id"])

                # Process input for the current node
                current_output = agent.process_input(input_data)

                # Step 4: Accumulate the output
                if isinstance(current_output, dict):
                    # Convert to string
                    current_output_str = json.dumps(current_output)
                else:
                    # Ensure it's a string
                    current_output_str = str(current_output)
                
                accumulated_output += current_output_str + " "

            # Step 5: Return the combined output
            return accumulated_output.strip()  # Strip any extra whitespace

        # Map edges to build the graph structure
        adjacency_list = {node["id"]: [] for node in self.setup["nodes"]}
        for edge in self.setup["edges"]:
            for target in edge["target"]:
                adjacency_list[edge["source"]].append(target)
                in_degree[target] += 1

        # Step 2: Begin processing using nodes with no dependencies (in_degree = 0)
        # Here, using the queue for nodes ready to be processed
        node_queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        initial_inputs = {node_id: input_data for node_id in node_queue}

        while node_queue:
            current_node_id = node_queue.pop(0)
            current_input = initial_inputs.get(current_node_id, "")

            # Find and execute the agent associated with the current node
            current_node = next(node for node in self.setup["nodes"] if node["id"] == current_node_id)
            current_agent = next(agent for agent in self.agents if agent.id == current_node_id)
            current_output = current_agent.process_input(current_input)

            # Store output
            memory[current_node_id] = current_output
            print(f"Processed Node {current_node_id}, Output: {current_output}")

            # Reduce in_degree of all connected nodes and append new ready nodes
            for target_node_id in adjacency_list[current_node_id]:
                if in_degree[target_node_id] > 0:
                    in_degree[target_node_id] -= 1
                    if in_degree[target_node_id] == 0:
                        node_queue.append(target_node_id)

                    # Prepare inputs for the target node
                    if target_node_id not in initial_inputs:
                        initial_inputs[target_node_id] = ""
                    initial_inputs[target_node_id] += current_output  # Append the current output

        # Assume the final node's output is the desired result
        final_node_id = self.setup["nodes"][-1]["id"]  # It's a heuristic, can be replaced with an explicit goal node
        return memory.get(final_node_id, ""), memory
        
                