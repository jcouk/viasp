from itertools import tee
from typing import Any, TypeVar, Iterable, Tuple, List
from collections import defaultdict
from types import MappingProxyType
from hashlib import sha1
from flask import current_app

import networkx as nx


def get_start_node_from_graph(graph: nx.DiGraph) -> Any:
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty")
    beginning = next(filter(lambda tuple: tuple[1] == 0, graph.in_degree()))
    return beginning[0]


def get_end_node_from_path(graph: nx.DiGraph) -> Any:
    end = next(filter(lambda tuple: tuple[1] == 0, graph.out_degree()))
    return end[0]


def get_leafs_from_graph(graph: nx.DiGraph) -> Iterable[Any]:
    for candidate, out_degree in graph.out_degree:
        if out_degree == 0:
            yield candidate

def get_root_node_from_graph(graph: nx.DiGraph) -> Any:
    return next(nx.topological_sort(graph))

def get_sorted_path_from_path_graph(graph: nx.DiGraph) -> Any:
    start = get_start_node_from_graph(graph)
    end = get_end_node_from_path(graph)
    return nx.shortest_path(graph, start, end)


T = TypeVar("T")


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def DefaultMappingProxyType() -> MappingProxyType[str, List]:
    return MappingProxyType(defaultdict())

def is_recursive(node, graph):
    """
    Checks if the node is recursive.
    :param node: The node to check.
    :param graph: The graph that contains the node.
    :return: True if the node is recursive, False otherwise.
    """
    nn = set(graph.nodes)
    if node in nn:
        return False
    else:
        for n in nn:
            if n.recursive != False and node in set(n.recursive.nodes):
                return True
            

def hash_from_sorted_transformations(sorted_program: List[Any]) -> str:
    hashes = [s.hash for s in sorted_program]
    concatenated = "".join(hashes)
    hash_object = sha1(concatenated.encode())
    return hash_object.hexdigest()

def hash_transformation_rules(rules: Tuple[Any, ...]) -> str:
    hash_object = sha1()
    for rule in rules:
        rule_str = current_app.json.dumps(rule)
        rule_hash = sha1(rule_str.encode()).hexdigest()
        hash_object.update(rule_hash.encode())
    return hash_object.hexdigest()