import json
from dataclasses import dataclass

from pytest import fixture

from tecton_gen_ai.fco import AgentClient, AgentService, prompt, tool
from tecton_gen_ai.testing.mocks import mock_batch_feature_view


@dataclass
class OpenAIConfig:
    model: str
    seed: int
    temperature: float
    response_format: dict

    def to_langchain_kwargs(self):
        return {
            "model": self.model,
            "seed": self.seed,
            "temperature": self.temperature,
            "model_kwargs": {"response_format": self.response_format},
        }

    def to_llamaindex_kwargs(self):
        return {
            "model": self.model,
            "additional_kwargs": {"response_format": self.response_format},
            "temperature": self.temperature,
        }


@fixture
def model_config():
    return OpenAIConfig(
        model="gpt-4o-2024-08-06",
        seed=0,
        temperature=0,
        response_format={"type": "json_object"},
    )


@fixture
def langchain_llm(model_config):
    import langchain
    from langchain_openai import ChatOpenAI

    langchain.debug = True

    return ChatOpenAI(**model_config.to_langchain_kwargs())


@fixture
def llamaindex_llm(model_config):
    from llama_index.llms.openai import OpenAI

    return OpenAI(**model_config.to_llamaindex_kwargs())


@fixture
def mock_agent_service(tecton_unit_test):
    user_info = mock_batch_feature_view(
        "user_info",
        {"user_id": "user2", "name": "Jim"},
        ["user_id"],
        description="Getting user name",
    )

    @prompt()
    def sys_prompt():
        return (
            # "You are serving user whose user_id " + user_id + ". "
            "The result should be in json format, the key is always 'result'"
        )

    @tool
    def get_tecton_employee_count() -> int:
        """
        Returns the number of employees in Tecton
        """
        return 110

    @tool
    def get_tecton_female_employee_count() -> int:
        """
        Returns the number of female employees in Tecton
        """
        return 60

    return AgentService(
        name="test",
        tools=[
            get_tecton_employee_count,
            get_tecton_female_employee_count,
            user_info,
        ],
        prompts=[sys_prompt],
    )


def test_langchain_agent(mock_agent_service, langchain_llm):
    client = AgentClient.from_local(mock_agent_service)
    res = client.invoke_agent(
        langchain_llm,
        "how many employees in tecton that are not female",
        system_prompt="sys_prompt",
        context={"user_id": "user2"},
    )
    assert json.loads(res)["result"] == 50

    agent = client.make_agent(langchain_llm, system_prompt="sys_prompt")
    with client.set_context({"user_id": "user2"}):
        res = agent.invoke({"input": "what is my name"})["output"]
    assert "jim" in json.loads(res)["result"].lower()


def test_llamaindex_agent(mock_agent_service, llamaindex_llm):
    client = AgentClient.from_local(mock_agent_service)
    res = client.invoke_agent(
        llamaindex_llm,
        "how many employees in tecton that are not female",
        system_prompt="sys_prompt",
        context={"user_id": "user2"},
    )
    assert json.loads(res)["result"] == 50

    agent = client.make_agent(llamaindex_llm, system_prompt="sys_prompt")
    with client.set_context({"user_id": "user2"}):
        res = str(agent.chat("what is my name"))
    assert "jim" in json.loads(res)["result"].lower()
