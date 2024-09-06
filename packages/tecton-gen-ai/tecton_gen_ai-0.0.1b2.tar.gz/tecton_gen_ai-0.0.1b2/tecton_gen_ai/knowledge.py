from typing import Any, Dict, List

from tecton import Attribute, Entity, FilteredSource, batch_feature_view
from tecton.types import Field, Int64, String

from tecton_gen_ai.utils.config_wrapper import to_json_config

from ._utils import set_serialization
from .deco import tool

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


def source_as_knowledge(
    source,
    vector_db_config,
    vectorize_column,
    feature_start_time,
    batch_schedule,
    timestamp_field,
    name=None,
    description=None,
    index_keys=None,
    secrets=None,
    **kwargs,
):
    if name is None:
        if isinstance(source, FilteredSource):
            name = source.source.name
        else:
            name = source.name
    if name is None or name == "":
        raise ValueError("name is required")
    if description is None:
        if isinstance(source, FilteredSource):
            description = source.source.description
        else:
            description = source.description
    if description is None or description == "":
        raise ValueError("description is required")
    sources = [source] if secrets is None else [source, secrets]
    vconf = to_json_config(vector_db_config)
    batch_deco = batch_feature_view(
        name=name + "_batch",
        sources=sources,
        entities=[
            Entity(
                name=name + "_" + vectorize_column,
                join_keys=[Field(vectorize_column, String)],
            )
        ],
        mode="pandas",
        offline=True,
        online=False,
        features=[
            Attribute(name="dummy", dtype=Int64),
        ],
        feature_start_time=feature_start_time,
        batch_schedule=batch_schedule,
        timestamp_field=timestamp_field,
        description=description,
        **kwargs,
    )

    def ingest(bs, *args):
        from langchain_core.vectorstores import VectorStore

        from tecton_gen_ai.utils.config_wrapper import from_json_config
        from tecton_gen_ai.utils.hashing import to_uuid

        if len(bs) == 0:
            return bs.assign(dummy=0)

        vs: VectorStore = from_json_config(vconf)
        texts = bs[vectorize_column].tolist()
        ids = [to_uuid(x) for x in texts]
        metadatas = bs[[x for x in bs.columns if x != timestamp_field]].to_dict(
            orient="records"
        )
        vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)

        return bs.head(1).assign(dummy=1)

    with set_serialization():
        if secrets is None:

            def ingest_0(bs):
                return ingest(bs)

            batch_fv = batch_deco(ingest_0)
        else:

            def ingest_1(bs, secrets):
                return ingest(bs, secrets)

            batch_fv = batch_deco(ingest_1)

    desc = f"""Search the knowledge base of {name}: {description}

Args:
query: the search query string
top_k: the top k results to return, default is {_DEFAULT_TOP_K}

Returns:

List[Dict[str, Any]]: search results
"""

    @tool(name=_SEARCH_TOOL_PREFIX + name, descripton=desc)
    def search(query: str, top_k: int = 5) -> "List[Dict[str, Any]]":
        """dummy"""

        from langchain_core.vectorstores import VectorStore

        from tecton_gen_ai.utils.config_wrapper import from_json_config

        vs: VectorStore = from_json_config(vconf)
        res = vs.similarity_search(query, top_k)

        jres = []
        for x in res:
            jres.append(x.metadata)
        return jres

    return batch_fv, search
