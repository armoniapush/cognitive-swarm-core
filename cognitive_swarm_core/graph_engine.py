"""
Graph Engine: Motor de consultas sobre grafos dirigidos ontológicos con NetworkX.
Agnóstico, desacoplado, con extracción K-Hop y serialización compacta orientada a prompts.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import networkx as nx


class GraphEngine:
    """Motor de consulta y serialización de subgrafos para inyección en prompts."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Añade un nodo tipado al grafo."""
        attrs = attributes or {}
        self.graph.add_node(node_id, **attrs)

    def add_edge(self, source: str, target: str, relation: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Añade una arista dirigida tipada."""
        attrs = dict(attributes) if attributes else {}
        attrs["relation"] = relation
        self.graph.add_edge(source, target, **attrs)

    def load_from_json(self, json_path: str | Path) -> None:
        """Carga el grafo desde un archivo JSON estructurado con 'nodes' y 'edges'."""
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo de grafo no encontrado: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.graph.clear()
        
        # Procesar nodos (soporta diccionario de nodos o lista)
        nodes_data = data.get("nodes", {})
        if isinstance(nodes_data, dict):
            for node_id, attrs in nodes_data.items():
                self.add_node(node_id, attrs)
        elif isinstance(nodes_data, list):
            for item in nodes_data:
                node_id = item.get("id")
                if node_id:
                    self.add_node(node_id, item)

        # Procesar aristas
        edges_data = data.get("edges", [])
        for edge in edges_data:
            src = edge.get("source")
            tgt = edge.get("target")
            rel = edge.get("relation", "relates_to")
            if src and tgt:
                self.add_edge(src, tgt, rel, edge)

    def save_to_json(self, output_path: str | Path) -> None:
        """Serializa el grafo a formato JSON ordenado."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        nodes_dict = {n: dict(data) for n, data in self.graph.nodes(data=True)}
        edges_list = [
            {"source": u, "target": v, **dict(data)}
            for u, v, data in self.graph.edges(data=True)
        ]

        payload = {
            "version": "1.0.0",
            "nodes": nodes_dict,
            "edges": edges_list
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def retrieve_subgraph(
        self,
        seed_nodes: List[str],
        max_hops: int = 2,
        max_tokens: int = 400
    ) -> str:
        """
        Recupera los vecinos dirigidos a k saltos de los nodos semilla y
        los serializa en un bloque conciso de texto apto para inyectar en prompt.
        """
        if not seed_nodes:
            return ""

        active_seeds = sorted([s for s in seed_nodes if s in self.graph])
        if not active_seeds:
            return "### CONTEXTO RELACIONAL OBLIGATORIO: [Sin nodos conexos identificados]"

        subgraph_nodes: Set[str] = set(active_seeds)
        current_frontier = set(active_seeds)

        for _ in range(max_hops):
            next_frontier = set()
            for node in sorted(current_frontier):
                # Vecinos salientes y entrantes deterministas
                succs = sorted(self.graph.successors(node))
                preds = sorted(self.graph.predecessors(node))
                neighbors = set(succs).union(set(preds))
                new_nodes = sorted(neighbors - subgraph_nodes)
                next_frontier.update(new_nodes)
                subgraph_nodes.update(new_nodes)
            current_frontier = next_frontier
            if not current_frontier:
                break

        lines = ["### CONTEXTO RELACIONAL OBLIGATORIO (SUBGRAFO ACTIVO):"]
        
        # Mapear primero las leyes y relaciones entre los nodos del subgrafo de forma determinista
        seen_edges = set()
        sorted_subgraph = sorted(subgraph_nodes)
        
        # Presupuesto acumulado de tokens aproximados
        char_limit = max_tokens * 4
        current_len = len(lines[0])

        for u in sorted_subgraph:
            for v in sorted(self.graph.successors(u)):
                if v in subgraph_nodes:
                    edge_key = (u, v)
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        data = self.graph.get_edge_data(u, v) or {}
                        rel = data.get("relation", "relates_to")
                        law = data.get("law") or data.get("rule")
                        u_name = self.graph.nodes[u].get("name", u)
                        v_name = self.graph.nodes[v].get("name", v)
                        
                        entry = f"- [{u_name}] --({rel})--> [{v_name}]"
                        if law:
                            entry += f"\n  REGLA DE FÍSICA / LEY: {law}"

                        # Verificación atómica de presupuesto
                        if current_len + len(entry) + 1 > char_limit:
                            lines.append("[... subgrafo delimitado por presupuesto de contexto]")
                            return "\n".join(lines)

                        lines.append(entry)
                        current_len += len(entry) + 1

        # Si no hay aristas internas, listar al menos las identidades de los nodos
        if len(lines) == 1:
            for n in sorted_subgraph:
                n_data = self.graph.nodes[n]
                n_name = n_data.get("name", n)
                n_rule = n_data.get("core_rule", "")
                entry = f"- Entidad: [{n_name}]"
                if n_rule:
                    entry += f" | Regla: {n_rule}"

                if current_len + len(entry) + 1 > char_limit:
                    lines.append("[... subgrafo delimitado por presupuesto de contexto]")
                    return "\n".join(lines)

                lines.append(entry)
                current_len += len(entry) + 1

        return "\n".join(lines)
