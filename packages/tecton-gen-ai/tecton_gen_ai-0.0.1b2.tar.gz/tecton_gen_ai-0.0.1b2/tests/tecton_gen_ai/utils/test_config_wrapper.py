from dataclasses import dataclass
from typing import Any

from pytest import raises

from tecton_gen_ai.utils.config_wrapper import (
    ExternalArgument,
    as_config,
    from_json_config,
    to_json_config,
)


@dataclass
class TestObj:
    """This is a test"""

    a: int
    b: Any

    def __eq__(self, other):
        return self.a == other.a and str(self.b) == str(other.b)

    def __str__(self):
        return f"TestObj(a={self.a}, b={self.b})"


def test_config_wrapper():
    TestObjConfig = as_config(TestObj)
    w = TestObjConfig(a=1, b="hello")
    assert w.target_type == TestObj
    assert w.instantiate() == TestObj(a=1, b="hello")
    from_json_config(w.to_json()) == TestObj(a=1, b="hello")

    w0 = TestObjConfig(a=1, b=None)
    w = TestObjConfig(a=1, b=w0)
    assert w.instantiate() == TestObj(a=1, b=TestObj(a=1, b=None))
    obj = from_json_config(to_json_config(w))
    assert obj == TestObj(a=1, b=TestObj(a=1, b=None))
    assert isinstance(obj.b, TestObj)

    w0 = TestObjConfig(a=ExternalArgument("x"), b=None)
    w = TestObjConfig(a=ExternalArgument("y"), b=w0)
    assert w.instantiate({"x": 1, "y": 2}) == TestObj(a=2, b=TestObj(a=1, b=None))
    with raises(KeyError):
        w.instantiate()
    from_json_config(w.to_json(), {"x": 1, "y": 2}) == TestObj(
        a=2, b=TestObj(a=1, b=None)
    )


def test_temp():
    from langchain_community.vectorstores.lancedb import LanceDB
    from langchain_openai import OpenAIEmbeddings

    LanceDBConf = as_config(LanceDB)
    OpenAIEmbeddingsConf = as_config(OpenAIEmbeddings)

    vdb = LanceDBConf(embedding=OpenAIEmbeddingsConf(), uri="sdf")
    assert isinstance(
        from_json_config(to_json_config(vdb)).embeddings, OpenAIEmbeddings
    )
