def validate_process_json(process_json):
    # Check if the root node exists
    if "name" not in process_json or "nodes" not in process_json:
        print(f"Error: Root node does not exist at path {process_json}.")
        return False

    nodes = process_json["nodes"]

    for i, node in enumerate(nodes):
        # Check if each node has required keys
        if "id" not in node or "assigned" not in node or "llm" not in node:
            print(f"Error: Node {i} does not have required keys at path {node}.")
            return False

        assigned = node["assigned"]
        llm = node["llm"]

        # Check if the assigned node has required keys
        if "label" not in assigned or "customName" not in assigned or "customType" not in assigned:
            print(f"Error: Node {i} 'assigned' dictionary does not have required keys at path {assigned}.")
            return False

        custom_config = assigned.get("customConfig", {})
        if ("system_prompt" not in custom_config and "sources" not in custom_config) or (len(custom_config) > 2):
            print(f"Error: Node {i} 'assigned' dictionary 'customConfig' has invalid keys at path {custom_config}.")
            return False

        # Check if the llm node has required keys
        if "selected" not in llm:
            print(f"Error: Node {i} 'llm' dictionary does not have required keys at path {llm}.")
            return False

    edges = process_json["edges"]

    #for i, edge in enumerate(edges):
    #    # Check if each edge has required keys
    #    if "source" not in edge or "target" not in edge:
    #        print(f"Error: Edge {i} does not have required keys at path {edge}.")
    #        return False

    return True

def validate_node(node):
    """
    Validates a single node based on its properties.

    :param node: The node to be validated.
    :return: True if the node is valid, False otherwise.
    """
    # Check if the node has required keys
    if "id" not in node or "assigned" not in node or "llm" not in node:
        print(f"Error: Node does not have required keys at path {node}.")
        return False

    assigned = node["assigned"]
    llm = node["llm"]

    # Check if the assigned node has required keys
    if "label" not in assigned or "customName" not in assigned or "customType" not in assigned:
        print(f"Error: Node 'assigned' dictionary does not have required keys at path {assigned}.")
        return False

    custom_config = assigned.get("customConfig", {})
    if ("system_prompt" not in custom_config and "sources" not in custom_config) or (len(custom_config) > 2):
        print(f"Error: Node 'assigned' dictionary 'customConfig' has invalid keys at path {custom_config}.")
        return False

    # Check if the llm node has required keys
    if "selected" not in llm:
        print(f"Error: Node 'llm' dictionary does not have required keys at path {llm}.")
        return False

    return True