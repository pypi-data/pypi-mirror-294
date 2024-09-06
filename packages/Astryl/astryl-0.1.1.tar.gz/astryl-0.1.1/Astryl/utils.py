
def build_batch_query(table_name, columns):
    properties = []
    for column in columns:
        default_value = "'Unknown'" if columns[column] == 'string' else "0"
        properties.append(f"{column}: COALESCE(node.{column}, {default_value})")
    
    newline = """,
"""
    properties_str = newline.join(properties)
    return f"""
    UNWIND $records AS node
    CREATE (n:{table_name.capitalize()} {{
        {properties_str}
    }})
    """

def node_to_dict(node):
    return {
        'id': node.id,
        'labels': list(node.labels),
        'properties': dict(node.items())
    }
    
def clean_node_properties(properties):
    cleaned_properties = {}
    for key, value in properties.items():
        if isinstance(value, float) and (value != value):
            cleaned_properties[key] = None
        else:
            cleaned_properties[key] = value
    return cleaned_properties
