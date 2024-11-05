import json



class MultiAgentSystem:
    def __init__(self, agent_setup="process.json"):

        with open(agent_setup, 'r') as f:
            self.setup = json.load(f)

        self.agents = []
        for node in self.setup["nodes"]:
            if node["assigned"]["customType"] == "AGENT":
                agent = LLMAgent(node)
            elif node["assigned"]["customType"] == "RAG":
                agent = RAGAgent(node)
            else:
                raise ValueError(f"Unsupported custom type: {node['customType']}")
            self.agents.append(agent)
            

    # Process the input data by visiting each node, processing it with its assigned agent,
    # and then exploring the connected agents. This function helps to simulate the behavior
    # of the multi-agent system.
    def process_input(self, input_data):
        # Initialize a set to keep track of visited nodes and an empty queue for nodes to be processed
        visited = set()
        node_queue = [(edge["source"], [next(n for n in self.setup["nodes"] if n["id"] == edge["source"])])
                   for edge in self.setup["edges"]] 
        while node_queue:
            # Dequeue a node and its path, check if it has been visited before
            node_id, path = node_queue.pop(0)
            if node_id not in visited:
                visited.add(node_id)    
                # Get the agent assigned to this node and process the input data with it
                agent = next(a for a in self.agents if a.id == node_id)
                input_data = agent.process_input(input_data)    
                # Find all connected agents of this node that haven't been visited yet
                connected_agents = self.get_connected_agents(node_id)
                for target_node_id in connected_agents:
                    if target_node_id not in visited:
                        # For each connected agent, find the edges that connect it to other nodes,
                        # and add them to the queue for further processing
                        for edge in self.setup["edges"]:
                            if edge["source"] == node_id and target_node_id in edge["target"]:
                                node_queue.append((edge["target"][0], path + [next(n for n in self.setup["nodes"] if n["id"] == edge["target"][0])]))   
        return input_data

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

