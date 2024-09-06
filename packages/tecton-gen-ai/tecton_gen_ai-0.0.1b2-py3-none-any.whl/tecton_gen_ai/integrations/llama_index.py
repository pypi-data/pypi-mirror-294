from typing import Any, Optional

from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent.runner.base import AgentRunner
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.llms.function_calling import FunctionCallingLLM

from ..agent.client import Agent, AgentClient, invoke_agent, make_agent


@invoke_agent.register(FunctionCallingLLM)
def _invoke_llama(
    llm: FunctionCallingLLM,
    client: AgentClient,
    message: str,
    system_prompt: Optional[str] = None,
    chat_history: Any = None,
    **kwargs: Any,
) -> str:
    runner = make_llama_index_agent_runner(llm, client, system_prompt, **kwargs)
    client.logger.debug(
        "Invoking LlamaIndex agent with message: %s, chat_history: %s",
        message,
        chat_history,
    )
    res = runner.chat(message, chat_history=chat_history)
    return str(res)


@make_agent.register(FunctionCallingLLM)
def make_llama_index_agent_runner(
    llm: FunctionCallingLLM,
    client: AgentClient,
    system_prompt: Optional[str] = None,
    **runner_kwargs: Any,
) -> AgentRunner:
    if system_prompt:
        if client.metastore.get(system_prompt).get("type") != "prompt":
            raise ValueError(f"{system_prompt} is not a prompt.")
    agent = _LlamaIndexAgent(client, llm, system_prompt=system_prompt)
    return agent.make_agent_runner(**runner_kwargs)


class _LlamaIndexAgent(Agent):
    def make_agent_runner(self, **kwargs):
        agent_worker = _TectonFunctionCallingAgentWorker.from_tools(
            self.tools,
            llm=self.llm,
            verbose=kwargs.get("verbose", False),
            allow_parallel_tool_calls=True,
            tecton_agent=self,
        )
        agent = agent_worker.as_agent(**kwargs)
        return agent

    def _make_tool(self, name):
        from llama_index.core.tools import FunctionTool

        f, descripton = self._get_dummy_func(name)
        _tool = FunctionTool.from_defaults(f, name=name, description=descripton)
        _tool._fn = lambda **kwargs: self.client.invoke_tool(name, kwargs)
        return _tool


class _TectonFunctionCallingAgentWorker(FunctionCallingAgentWorker):
    def __init__(self, *args, tecton_agent: _LlamaIndexAgent, **kwargs):
        super().__init__(*args, **kwargs)
        self._tecton_agent = tecton_agent

    def _make_messages(self, question, history):
        history = history or []
        history = self._add_sys_prompt(history)
        return history + [("human", question)]

    def get_all_messages(self, task):
        if self._tecton_agent._system_prompt:
            sys_prompt = self._tecton_agent.invoke_sys_prompt()
            self.prefix_messages = [
                ChatMessage(role=MessageRole.SYSTEM, content=sys_prompt)
            ]
        else:
            self.prefix_messages = []
        return super().get_all_messages(task)
