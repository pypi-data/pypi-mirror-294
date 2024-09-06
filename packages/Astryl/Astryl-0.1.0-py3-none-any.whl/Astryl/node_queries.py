
def pullNodes(label, connection, db_name, limit=25):
    query = f"""
    MATCH (n:{label})
    RETURN n
    LIMIT {limit}
    """
    nodes = []
    
    # Execute the query
    with connection.session(database=db_name) as session:
        result = session.run(query)
        
        # Extract nodes into a list of dictionaries
        nodes = [{'id': record['n'].id, **record['n']._properties} for record in result]
        
    return nodes

    
# Fetch all nodes of a label
def get_all_nodes(label, session, limit=250):
    query = f"MATCH (result:{label}) RETURN result limit {limit}"
    result = session.run(query)
    nodes = []
    for record in result:
        node = record["result"]
        # Directly access the frozenset of labels
        node_labels = node.labels
        node_label = next(iter(node_labels), None)  # Get the first label if available
        nodes.append({"id": node.id, "properties": dict(node.items()), "label": node_label})
    return nodes


def get_related_nodes(current, nodeId, relationship, direction, db_name, driver):
    with driver.session(database=db_name) as session:
        # Adjust the Cypher query based on the direction
        if direction == "incoming":
            query = f"""
                MATCH (n:{current}) <-[r:{relationship}]- (result)
                WHERE id(n) = {nodeId}
                RETURN result
                LIMIT 25
            """
        elif direction == "outgoing":
            query = f"""
                MATCH (n:{current}) -[r:{relationship}]-> (result)
                WHERE id(n) = {nodeId}
                RETURN result
                LIMIT 25
            """
        else:
            raise ValueError("Invalid direction: must be 'incoming' or 'outgoing'")

        result = session.run(query)
        
        nodes = []
        for record in result:
            node = record["result"]
            node_properties = dict(node.items())
            cleaned_properties = clean_node_properties(node_properties)
            node_labels = node.labels
            node_label = next(iter(node_labels), None)  # Get the first label if available
            nodes.append({"id": node.id, "properties": cleaned_properties, "label": node_label})
        return nodes

def get_distinct_relationship_types(node, node_id, db_name, driver):
    with driver.session(database=db_name) as session:
        result_incoming = session.run(f"""
            MATCH (n:{node})<-[r]-()
            WHERE id(n) = {node_id}
            RETURN DISTINCT type(r) AS relationship_type
        """)
        
        result_outgoing = session.run(f"""
            MATCH (n:{node})-[r]->()
            WHERE id(n) = {node_id}
            RETURN DISTINCT type(r) AS relationship_type
        """)
        
        incoming_relationship_types = [record["relationship_type"] for record in result_incoming]
        outgoing_relationship_types = [record["relationship_type"] for record in result_outgoing]
        
        return {
            "incoming": incoming_relationship_types or ["No incoming relationships"],
            "outgoing": outgoing_relationship_types or ["No outgoing relationships"]
        }
        
def clean_node_properties(properties):
    cleaned_properties = {}
    for key, value in properties.items():
        if isinstance(value, float) and (value != value):  # Check if the value is NaN
            cleaned_properties[key] = None
        else:
            cleaned_properties[key] = value
    return cleaned_properties
