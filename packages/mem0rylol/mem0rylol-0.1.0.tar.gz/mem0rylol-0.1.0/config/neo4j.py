# config/neo4j.py
from neo4j import GraphDatabase

def get_neo4j_client(uri, username, password):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver

def close_neo4j_client(driver):
    if driver is not None:
        driver.close()