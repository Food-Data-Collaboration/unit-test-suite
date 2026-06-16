"""RDFLib-based test adapter for DFC/JSON-LD interop tests."""

import json
from typing import Any

from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, XSD

from .adapter import TestAdapter

DFC_B = Namespace("http://static.datafoodconsortium.org/ontologies/DFC_BusinessOntology.owl#")
DFC_M = Namespace("http://static.datafoodconsortium.org/data/measures.rdf#")
DFC_PT = Namespace("http://static.datafoodconsortium.org/data/productTypes.rdf#")


class RDFLibAdapter(TestAdapter):
    """RDFLib-based implementation of the test adapter."""

    @property
    def platform_name(self) -> str:
        return "python-rdflib"

    def parse_jsonld(self, data: dict[str, Any]) -> Graph:
        """Parse JSON-LD into an RDFLib Graph."""
        g = Graph()
        g.parse(data=json.dumps(data), format="json-ld")
        return g

    def serialize_jsonld(self, graph: Graph) -> dict[str, Any]:
        """Serialize an RDFLib Graph back to JSON-LD."""
        result = graph.serialize(format="json-ld", context=str(DFC_B))
        return json.loads(result)

    def validate(self, data: dict[str, Any]) -> list[str]:
        """Validate JSON-LD document (basic structural validation)."""
        errors = []

        if "@context" not in data and "@graph" not in data:
            errors.append("Missing @context")

        if "@graph" in data:
            for i, node in enumerate(data["@graph"]):
                if "@type" not in node and "@id" not in node:
                    errors.append(f"Node {i} missing @type and @id")
        elif "@type" not in data:
            errors.append("Document missing @type")

        return errors

    def expand(self, data: dict[str, Any]) -> Any:
        """Expand JSON-LD using RDFLib."""
        g = Graph()
        g.parse(data=json.dumps(data), format="json-ld")
        return g

    def compact(self, graph: Graph, context: dict[str, Any]) -> dict[str, Any]:
        """Compact expanded JSON-LD (simplified implementation)."""
        return self.serialize_jsonld(graph)

    def flatten(self, data: dict[str, Any]) -> dict[str, Any]:
        """Flatten JSON-LD (simplified implementation)."""
        g = Graph()
        g.parse(data=json.dumps(data), format="json-ld")

        flattened = {"@context": data.get("@context", {}), "@graph": []}

        for subject in g.subjects():
            node = {}
            if isinstance(subject, BNode):
                node["@id"] = f"_:b{hash(subject) % 1000}"
            else:
                node["@id"] = str(subject)

            for pred, obj in g.predicate_objects(subject):
                pred_str = str(pred)
                if pred == RDF.type:
                    node["@type"] = pred_str
                else:
                    if pred_str not in node:
                        node[pred_str] = []
                    if isinstance(obj, Literal):
                        node[pred_str].append({"@value": str(obj)})
                    else:
                        node[pred_str].append({"@id": str(obj)})

            flattened["@graph"].append(node)

        return flattened
