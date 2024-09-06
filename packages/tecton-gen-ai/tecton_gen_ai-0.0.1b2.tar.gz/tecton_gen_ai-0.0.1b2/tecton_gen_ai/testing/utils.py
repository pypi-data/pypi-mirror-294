import shutil
from typing import Any

from tecton_gen_ai.utils.config_wrapper import as_config


def create_testing_vector_db_config(path: str, remove_if_exists: bool) -> Any:
    if remove_if_exists:
        shutil.rmtree(path, ignore_errors=True)

    from langchain_community.vectorstores.lancedb import LanceDB
    from langchain_openai import OpenAIEmbeddings

    LanceDBConf = as_config(LanceDB)
    OpenAIEmbeddingsConf = as_config(OpenAIEmbeddings)

    vdb = LanceDBConf(embedding=OpenAIEmbeddingsConf(), uri=path)
    return vdb
