import json
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from functools import singledispatch

# for executing function declarations
from typing import Any, Dict, List, Optional, Tuple  # noqa

import pandas as pd
from tecton import BatchFeatureView, RealtimeFeatureView

from tecton_gen_ai.utils.log import NOOP_LOGGER

from .service import AgentService

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


@singledispatch
def invoke_agent(
    llm,
    client: "AgentClient",
    message: str,
    system_prompt: Optional[str] = None,
    chat_history: Any = None,
    **kwargs: Any,
):
    raise NotImplementedError(f"Unsupported type {type(llm)}")


@singledispatch
def make_agent(
    llm,
    client: "AgentClient",
    system_prompt: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    raise NotImplementedError(f"Unsupported type {type(llm)}")


class AgentClient:
    def __init__(self):
        self._current_context = ContextVar("current_context", default=None)
        self._current_logger = ContextVar("current_context", default=NOOP_LOGGER)

    @staticmethod
    def from_remote(
        url: str, workspace: str, service: str, api_key: str
    ) -> "AgentClient":
        return _AgentClientRemote(url, workspace, service, api_key)

    @staticmethod
    def from_local(service: AgentService) -> "AgentClient":
        return _AgentClientLocal(service)

    @property
    def logger(self) -> logging.Logger:
        return self._current_logger.get()

    @contextmanager
    def set_logger(self, logger: logging.Logger):
        token = self._current_logger.set(logger)
        try:
            yield
        finally:
            self._current_logger.reset(token)

    @contextmanager
    def set_context(self, context: Optional[Dict[str, Any]]):
        self.logger.debug("Setting context to %s", context)
        token = self._current_context.set(context or {})
        try:
            yield
        finally:
            self._current_context.reset(token)

    def make_agent(
        self, llm: Any, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> Any:
        _load_dependencies()
        return make_agent(llm, self, system_prompt=system_prompt, **kwargs)

    def invoke_agent(
        self,
        llm: Any,
        message: str,
        system_prompt: Optional[str] = None,
        chat_history: Any = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> str:
        _load_dependencies()
        func = lambda: invoke_agent(  # noqa
            llm,
            self,
            message=message,
            system_prompt=system_prompt,
            chat_history=chat_history,
            **kwargs,
        )

        if context is not None:
            with self.set_context(context):
                res = func()
        else:
            res = func()
        self.logger.debug("Result of invoking agent: %s", res)
        return res

    def _get_context(self) -> Dict[str, Any]:
        return (self._current_context.get() or {}).copy()

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any]
    ):
        raise NotImplementedError

    @property
    def metastore(self):
        return self._invoke("metastore", [], [], {})

    def invoke_tool(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        kwargs = kwargs or {}
        self.logger.debug("Invoking tool %s with %s", name, kwargs)
        meta = self.metastore[name]
        if meta["type"] == "fv_tool":
            return self.invoke_feature_view(name, kwargs)
        ctx = self._get_context()
        ctx.update(kwargs)
        entity_args = meta.get("entity_args", [])
        llm_args = meta.get("llm_args", [])
        return self._invoke(name, entity_args, llm_args, ctx)

    def invoke_feature_view(
        self, name: str, kwargs: Optional[Dict[str, Any]] = None
    ) -> Any:
        kwargs = kwargs or {}
        self.logger.debug("Invoking feature view as tool %s with %s", name, kwargs)
        tool_name = "fv_tool_" + name
        tool = self.metastore[name]

        ctx = self._get_context()
        ctx.update(kwargs)
        key_map = {k: ctx[k] for k in tool["schema"].keys()}

        return self._get_feature_value(tool_name, key_map, {})

    def invoke_prompt(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        kwargs = kwargs or {}
        self.logger.debug("Invoking prompt %s with %s", name, kwargs)
        ctx = self._get_context()
        ctx.update(kwargs)
        metastore = self.metastore
        entity_args = metastore[name].get("entity_args", [])
        llm_args = metastore[name].get("llm_args", [])
        return self._invoke(name, entity_args, llm_args, kwargs)

    def search(self, name, query: str, top_k: int = _DEFAULT_TOP_K):
        self.logger.debug("Searching %s with query %s", name, query)
        if query == "":
            return []
        return self.invoke_tool(
            _SEARCH_TOOL_PREFIX + name,
            dict(query=query, top_k=top_k),
        )

    def _invoke(self, name, entity_args, llm_args, kwargs):
        ctx_map = {}
        key_map = {}
        for k, v in kwargs.items():
            if k in entity_args:
                key_map[k] = v
            # elif k not in llm_args:
            #    raise ValueError(f"Unknown argument {k}")
            if k in llm_args:
                ctx_map[k] = v

        result = self._get_feature_value(name, key_map, ctx_map)
        self.logger.debug("Result of %s: %s", name, result)
        return result


class _AgentClientRemote(AgentClient):
    def __init__(self, url: str, workspace: str, service: str, api_key: str):
        super().__init__()
        from tecton_client import TectonClient

        self.client = TectonClient(
            url, api_key=api_key, default_workspace_name=workspace
        )
        self.service = service

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any]
    ):
        gf = self.client.get_features(
            feature_service_name=self.service + "_" + name,
            join_key_map=key_map,
            request_context_map={
                "name": name,
                "input": json.dumps(request_map),
            },
        )
        resp = json.loads(gf.get_features_dict()[name + ".output"])
        if "error" in resp:
            raise Exception(resp["error"])
        result = resp["result"]
        return result


class _AgentClientLocal(AgentClient):
    def __init__(self, service: AgentService):
        super().__init__()
        self.service = service
        self.tool_map = {tool.name: tool for tool in service.online_fvs}

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any]
    ):
        fv: RealtimeFeatureView = self.tool_map[name]
        res = dict(key_map)
        res.update(
            {
                "name": name,
                "input": json.dumps(request_map),
            }
        )
        if len(fv.sources) > 1:
            bfv: BatchFeatureView = fv.sources[1].feature_definition
            res[bfv.get_timestamp_field()] = datetime.now()
        odf = fv.get_features_for_events(pd.DataFrame([res])).to_pandas()
        resp = json.loads(odf[name + "__output"].iloc[0])
        if "error" in resp:
            raise Exception(resp["error"])
        result = resp["result"]
        return result


class Agent:
    def __init__(self, client: AgentClient, llm, system_prompt=None) -> None:
        self.client = client
        self.llm = llm
        self._system_prompt = system_prompt
        self.tools = self._make_tools()

    def invoke(self, question, history=None, context=None, kwargs=None) -> str:
        raise NotImplementedError

    def invoke_sys_prompt(self):
        context = self.client._get_context()
        if not self._system_prompt:
            raise ValueError("No system prompt provided.")
        name = self._system_prompt
        value = self.client.metastore.get(name)
        match = all(key in context for key in value.get("keys", [])) and all(
            key in context for key in value.get("args", [])
        )
        if not match:
            raise ValueError(
                f"Context does not have all required keys for system prompt {name}."
            )
        if len(context) > 0:
            prefix = f"All context in the system: {context}\n\n"
        else:
            prefix = ""
        prompt = self.client.invoke_prompt(name, context)
        return prefix + prompt

    def _add_sys_prompt(self, history):
        if not self._system_prompt:
            return history
        sys_prompt = ("system", self.invoke_sys_prompt())
        history.insert(0, sys_prompt)
        return history

    def _get_dummy_func(self, name):
        meta = self.client.metastore[name]
        if meta["type"] == "tool":
            code = meta["def"]
        elif meta["type"] == "fv_tool":
            queryable = meta.get("queryable", True)
            schema = meta["schema"] if queryable else {}
            params = ",".join(f"{k}:{v}" for k, v in schema.items())
            code = f"def {name}({params}) -> 'Dict[str,Any]':\n    pass"
        else:
            raise ValueError(f"Unknown tool type {meta['type']}")
        exec(code, globals(), locals())
        descripton = meta.get("description")
        return locals()[name], descripton

    def _make_tool(self, name):
        raise NotImplementedError

    def _make_tools(self):
        return [
            self._make_tool(name)
            for name, value in self.client.metastore.items()
            if value["type"] in ["tool", "fv_tool"]
        ]


def _load_dependencies():
    try:
        from tecton_gen_ai.integrations import langchain  # noqa
    except ImportError:
        pass

    try:
        from tecton_gen_ai.integrations import llama_index  # noqa
    except ImportError:
        pass
