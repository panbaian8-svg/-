"""
Knowledge graph service
"""
import networkx as nx
from typing import Dict, Any, List, Tuple
import json


class GraphService:
    """Service for building and querying knowledge graphs"""

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, knowledge: Dict[str, Any]) -> nx.DiGraph:
        """
        Build knowledge graph from structured knowledge

        Args:
            knowledge: Structured knowledge from knowledge extraction

        Returns:
            NetworkX graph
        """
        self.graph = nx.DiGraph()

        chapters = knowledge.get("chapters", [])

        for chapter in chapters:
            chapter_id = chapter.get("id")
            chapter_title = chapter.get("title", "")

            # Add chapter node
            self.graph.add_node(
                chapter_id,
                label=chapter_title,
                type="chapter"
            )

            topics = chapter.get("topics", [])

            for topic in topics:
                topic_id = topic.get("id")
                topic_title = topic.get("title", "")

                # Add topic node
                self.graph.add_node(
                    topic_id,
                    label=topic_title,
                    type="topic"
                )

                # Add edge from chapter to topic
                self.graph.add_edge(
                    chapter_id,
                    topic_id,
                    relation="contains"
                )

                # Add formulas
                formulas = topic.get("formulas", [])
                for formula in formulas:
                    formula_id = formula.get("id")
                    formula_content = formula.get("content", "")

                    self.graph.add_node(
                        formula_id,
                        label=formula_content,
                        type="formula"
                    )

                    self.graph.add_edge(
                        topic_id,
                        formula_id,
                        relation="contains"
                    )

                # Add examples
                examples = topic.get("examples", [])
                for example in examples:
                    example_id = example.get("id")
                    example_content = example.get("content", "")

                    self.graph.add_node(
                        example_id,
                        label=example_content,
                        type="example"
                    )

                    self.graph.add_edge(
                        topic_id,
                        example_id,
                        relation="contains"
                    )

        return self.graph

    def get_nodes_and_edges(self) -> Dict[str, List]:
        """
        Get nodes and edges for visualization

        Returns:
            Dict with nodes and edges lists
        """
        nodes = []
        for node_id in self.graph.nodes:
            node_data = self.graph.nodes[node_id]
            nodes.append({
                "id": node_id,
                "label": node_data.get("label", node_id),
                "type": node_data.get("type", "node")
            })

        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                "source": source,
                "target": target,
                "label": data.get("relation", "")
            })

        return {
            "nodes": nodes,
            "edges": edges
        }

    def get_related_topics(self, topic_id: str) -> List[str]:
        """
        Get related topics for a given topic

        Args:
            topic_id: Topic ID

        Returns:
            List of related topic IDs
        """
        if topic_id not in self.graph:
            return []

        # Get predecessors and successors
        related = list(self.graph.predecessors(topic_id))
        related.extend(list(self.graph.successors(topic_id)))

        return list(set(related))

    def get_path(self, source_id: str, target_id: str) -> List[str]:
        """
        Get path between two nodes

        Args:
            source_id: Source node ID
            target_id: Target node ID

        Returns:
            List of node IDs in path
        """
        try:
            return nx.shortest_path(self.graph, source_id, target_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
