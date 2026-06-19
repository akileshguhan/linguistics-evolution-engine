from neo4j import GraphDatabase
from core.config import config
from typing import List, Dict, Any

class Neo4jClient:
    def __init__(self):
        # Establish connection with Neo4j AuraDB instance using credentials from Config
        self.driver = GraphDatabase.driver(
            config.NEO4J_URI, 
            auth=(config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def clear_database(self):
        """Resets the graph workspace for a fresh game/simulation run."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def initialize_proto_words(self, words: List[str]):
        """Creates the initial baseline text nodes in Neo4j at Epoch 0."""
        query = """
        CREATE (w:WordNode {text: $text, epoch: 0, root_word: $text})
        RETURN id(w) as node_id
        """
        with self.driver.session() as session:
            for word in words:
                session.run(query, text=word)

    def create_mutation_step(self, parent_word: str, parent_epoch: int, child_word: str, root_word: str, edge_metadata: Dict[str, Any]):
        """
        Generates a child WordNode representing the next generation of evolution,
        and binds it to its parent via a MUTATED_BY edge carrying vector metadata.
        """
        query = """
        MATCH (p:WordNode {text: $parent_word, epoch: $parent_epoch, root_word: $root_word})
        CREATE (c:WordNode {text: $child_word, epoch: $child_epoch, root_word: $root_word})
        CREATE (p)-[r:MUTATED_BY {
            event: $event, 
            isolation: $isolation, 
            density: $density,
            literacy: $literacy,
            climate: $climate
        }]->(c)
        RETURN id(c) as child_id
        """
        with self.driver.session() as session:
            session.run(
                query,
                parent_word=parent_word,
                parent_epoch=parent_epoch,
                child_word=child_word,
                child_epoch=parent_epoch + 1,
                root_word=root_word,
                event=edge_metadata.get("event", "natural_drift"),
                isolation=float(edge_metadata.get("isolation", 0.0)),
                density=float(edge_metadata.get("density", 0.0)),
                literacy=float(edge_metadata.get("literacy", 0.5)),
                climate=float(edge_metadata.get("climate", 0.5))
            )

    def get_complete_tree(self) -> List[Dict[str, Any]]:
        """
        Fetches every node and mutation path in the database.
        """
        query = """
        MATCH (n:WordNode)
        OPTIONAL MATCH (n)-[r:MUTATED_BY]->(m:WordNode)
        RETURN n.text as source, n.epoch as source_epoch, n.root_word as root,
               m.text as target, m.epoch as target_epoch, 
               r.event as event, r.isolation as isolation, r.density as density,
               r.literacy as literacy, r.climate as climate
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

    def get_epoch_state(self, epoch_id: int) -> List[Dict[str, Any]]:
        """
        Fetches all nodes that exist at a specific epoch for branching.
        """
        query = """
        MATCH (n:WordNode {epoch: $epoch_id})
        RETURN n.text as text, n.epoch as epoch, n.root_word as root_word
        """
        with self.driver.session() as session:
            result = session.run(query, epoch_id=epoch_id)
            return [record.data() for record in result]