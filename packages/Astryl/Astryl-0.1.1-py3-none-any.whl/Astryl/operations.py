from pandas import read_sql
from neo4j.exceptions import ServiceUnavailable

def createNodesFromNodeAttribute(labelFrom, attributeName, labelTo, db_name, connection):
    query = f"""
    MATCH (n:{labelFrom})
    WITH DISTINCT n.{attributeName} AS attributeValue
    WHERE attributeValue IS NOT NULL
    MERGE (m:{labelTo} {{id: attributeValue}})
    """
    with connection.session(database=db_name) as session:
        session.run(query)


def createRelationshipBetweenNodes(labelFrom, attributeFrom, labelTo, attributeTo, relationshipType, db_name, connection):
    query = f"""
    MATCH (a:{labelFrom}), (b:{labelTo})
    WHERE a.{attributeFrom} = b.{attributeTo}
    MERGE (a)-[r:{relationshipType}]->(b)
    """
    with connection.session(database=db_name) as session:
        session.run(query)


def removeNodesWithNoRelationships(label, db_name, connection):
    query = f"""
    MATCH (n:{label})
    WHERE NOT (n)-[]-()
    DELETE n
    """
    with connection.session(database=db_name) as session:
        session.run(query)

def findOrCreateNodeByAttribute(label, attribute, value, db_name, connection):
    query = f"""
    MERGE (n:{label} {{ {attribute}: '{value}' }})
    RETURN n
    """
    with connection.session(database=db_name) as session:
        result = session.run(query)
        return result.single()[0]

def execute_neo4j_query(driver, query, parameters, db):
    with driver.session(database=db) as session:
        result = session.run(query, parameters)
    return result

def get_neo4j_databases(driver,db):
    try:
        with driver.session(database=db) as session:
            result = session.run("SHOW DATABASES")
            databases = [record["name"] for record in result]
        driver.close()
        return databases
    except ServiceUnavailable as e:
        return []
    
