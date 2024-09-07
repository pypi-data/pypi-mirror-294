from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum
import hashlib
from typing import Dict, Any, List
from sycamore.plan_nodes import Node
from sycamore.transforms.map import Map
from sycamore.data import HierarchicalDocument
from sycamore.llms import LLM
from pydantic import BaseModel, create_model
import asyncio

import json
import uuid
import logging

logger = logging.getLogger(__name__)


class GraphRelationshipExtractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract(self, doc: "HierarchicalDocument") -> "HierarchicalDocument":
        pass


class RelationshipExtractor(GraphRelationshipExtractor):
    """
    Extracts relationships between entities found in each child of a document.

    Args:
        llm: OpenAI model that is compatable with structured outputs(gpt-4o-mini)
        relationships: list of entities in the form of pydantic schemas to be extracted
        split_calls: A boolean that if true, calls the LLM for each entity instead of batching them in one call

    """

    def __init__(self, llm: LLM, relationships: list[BaseModel] = [], split_calls: bool = False):
        self.relationships = self._serialize_relationships(relationships)
        self.llm = llm
        self.split_calls = split_calls

    def extract(self, doc: HierarchicalDocument) -> HierarchicalDocument:
        async def gather_api_calls():
            tasks = [self._generate_relationships(child) for child in doc.children]
            res = await asyncio.gather(*tasks)
            return res

        res = asyncio.run(gather_api_calls())

        for i, section in enumerate(doc.children):
            for label, relations in res[i].items():
                for relation in relations:
                    start_hash = hashlib.sha256(json.dumps(relation["start"]).encode()).hexdigest()
                    end_hash = hashlib.sha256(json.dumps(relation["end"]).encode()).hexdigest()

                    start_exists = section["properties"]["nodes"][relation["start_label"]].get(start_hash, None)
                    end_exists = section["properties"]["nodes"][relation["end_label"]].get(end_hash, None)
                    if not (start_exists and end_exists):
                        logger.warn(
                            f"""
                            Entities referenced by relationship does not exist:
                            Start: {relation["start"]}
                            End: {relation["end"]}
                            """
                        )
                        continue

                    rel: Dict[str, Any] = {
                        "TYPE": label,
                        "properties": {},
                        "START_HASH": start_hash,
                        "START_LABEL": relation["start_label"],
                    }

                    for key, value in relation.items():
                        if key not in ["start", "end", "start_label", "end_label"]:
                            rel["properties"][key] = value

                    section["properties"]["nodes"][relation["end_label"]][end_hash]["relationships"][
                        str(uuid.uuid4())
                    ] = rel
        return doc

    def _serialize_relationships(self, entities):
        from sycamore.utils.pickle_pydantic import safe_cloudpickle

        serialized = []
        for entity in entities:
            serialized.append(safe_cloudpickle(entity))
        return serialized

    def _deserialize_relationships(self):
        from sycamore.utils.pickle_pydantic import safe_cloudunpickle

        deserialized = []
        for entity in self.relationships:
            deserialized.append(safe_cloudunpickle(entity))

        return deserialized

    async def _generate_relationships(self, section: HierarchicalDocument) -> dict:
        relations = self._deserialize_relationships()
        parsed_relations = []
        parsed_metadata = {}
        for relation in relations:
            start_label = relation.__annotations__["start"].__name__
            end_label = relation.__annotations__["end"].__name__

            start_nodes = [
                json.dumps(node["raw_entity"]) for node in section["properties"]["nodes"].get(start_label, {}).values()
            ]
            end_nodes = [
                json.dumps(node["raw_entity"]) for node in section["properties"]["nodes"].get(end_label, {}).values()
            ]

            relation.__annotations__["start"] = Enum(start_label, {entity: entity for entity in start_nodes})
            relation.__annotations__["end"] = Enum(end_label, {entity: entity for entity in end_nodes})

            if start_nodes and end_nodes:
                parsed_relations.append(relation)
                parsed_metadata[relation.__name__] = {
                    "start_label": start_label,
                    "end_label": end_label,
                    "start_nodes": set(start_nodes),
                    "end_nodes": set(end_nodes),
                }

        if not parsed_relations:
            return {}

        # Use mypy ignore type since pydantic has bad interaction with mypy with creating class from a variable class
        # (List[relation], ...) is weird notation required by pydantic, sorry - Ritam
        # https://docs.pydantic.dev/latest/concepts/models/#required-fields
        fields = {relation.__name__: (List[relation], ...) for relation in parsed_relations}  # type: ignore

        models, entities_list = self._build_llm_call_params(fields, parsed_metadata)

        assert len(models) == len(entities_list)
        outputs = []
        for i in range(len(models)):
            llm_kwargs = {"response_format": models[i]}
            prompt_kwargs = {"prompt": str(GraphRelationshipExtractorPrompt(section.data["summary"], entities_list[i]))}
            outputs.append(await self.llm.generate_async(prompt_kwargs=prompt_kwargs, llm_kwargs=llm_kwargs))

        async def _process_llm_output(outputs: list[str], parsed_metadata: dict, summary: str):
            parsed_res: dict[str, Any] = {}
            for output in outputs:
                try:
                    parsed_res |= json.loads(output)
                except json.JSONDecodeError:
                    logger.warn("LLM Output failed to be decoded to JSON")
                    logger.warn("Input: " + summary)
                    logger.warn("Output: " + output)
                    return {}

            for label, relations in parsed_res.items():
                for relation in relations:
                    relation["start_label"] = parsed_metadata[label]["start_label"]
                    relation["end_label"] = parsed_metadata[label]["end_label"]

            return parsed_res

        return await _process_llm_output(outputs, parsed_metadata, section.data["summary"])

    def _build_llm_call_params(self, fields, parsed_metadata):
        models = []
        entities_list = []
        if self.split_calls:
            for field_name, field_value in fields.items():
                models.append(create_model("relationships", __base__=BaseModel, **{field_name: field_value}))
                entities = []
                entities.append(f"""{parsed_metadata[field_name]["start_label"]}:\n""")
                entities.extend([f"{node}\n" for node in parsed_metadata[field_name]["start_nodes"]])
                entities.append(f"""{parsed_metadata[field_name]["end_label"]}:\n""")
                entities.extend([f"{node}\n" for node in parsed_metadata[field_name]["end_nodes"]])
                entities_list.append("".join(entities))
        else:
            models.append(create_model("relationships", __base__=BaseModel, **fields))
            parsed_entities = defaultdict(lambda: set())
            for key, value in parsed_metadata.items():
                parsed_entities[value["start_label"]] |= value["start_nodes"]
                parsed_entities[value["end_label"]] |= value["end_nodes"]

            entities = []
            for key, nodes in parsed_entities.items():
                entities.append(f"{key}:\n")
                for node in nodes:
                    entities.append(f"{node}\n")
            entities_list.append("".join(entities))

        return models, entities_list


def GraphRelationshipExtractorPrompt(query, entities):
    return f"""
    -Goal-
    You are a helpful information extraction system.

    You will be given a sequence of data in different formats(text, table, Section-header) in order.
    Your job is to extract relationships that map between entities that have already been extracted from this text.

    -Real Data-
    ######################
    Entities: {entities}
    Text: {query}
    ######################
    Output:"""


class ExtractRelationships(Map):
    """
    Extracts features determined by a specific extractor from each document
    """

    def __init__(self, child: Node, extractor: RelationshipExtractor, **resource_args):
        super().__init__(child, f=extractor.extract, **resource_args)
