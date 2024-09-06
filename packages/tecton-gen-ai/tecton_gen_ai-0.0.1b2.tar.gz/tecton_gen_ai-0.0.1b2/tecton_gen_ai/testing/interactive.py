import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Callable, Iterator, Optional

import ipywidgets as widgets
from IPython.display import Markdown, display

from tecton_gen_ai.agent import AgentClient
from tecton_gen_ai.utils.log import NOOP_LOGGER

_WIDGET_LOGGER = ContextVar("widget_logger", default=NOOP_LOGGER)


def qna(
    client: AgentClient,
    llm: Any,
    system_prompt: Any = None,
    context: Any = None,
    debug: bool = True,
) -> Any:
    def _run(message: str) -> str:
        logger = get_widget_logger()
        logger.setLevel(logging.DEBUG)
        with client.set_logger(logger):
            return client.invoke_agent(
                llm, message, system_prompt=system_prompt, context=context
            )

    return single_turn(_run, realtime=False, markdown=True, debug=debug)


def auto_complete(
    client: AgentClient,
    search_name: str,
    handle: Any,
    top_k: int = 5,
    debug: bool = False,
) -> Any:
    if isinstance(handle, str):
        def _handle(x):
            return x[handle]
    elif handle is None:
        def _handle(x):
            return str(x)
    else:
        _handle = handle
    return single_turn(
        lambda x: "\n".join(_handle(x) for x in client.search(search_name, x, top_k)),
        realtime=True,
        markdown=False,
        debug=debug,
    )


def single_turn(
    on_compute: Callable[[str], str],
    realtime: bool = False,
    markdown: bool = False,
    debug: bool = True,
) -> Any:
    # Create a text input widget
    text_input = widgets.Text(
        value="",
        placeholder="Type something",
        disabled=False,
        continuous_update=realtime,
    )

    output = widgets.Output()
    debugo = widgets.Output()

    def on_event(change):
        with output:
            if not realtime:
                output.clear_output()
                display(Markdown("Generating response..."))
        with set_widget_logger(debugo if debug else None):
            res = on_compute(change["new"])
        with output:
            output.clear_output()
            if markdown:
                display(Markdown(res))
            else:
                print(res)

    text_input.observe(on_event, names="value")

    items = [text_input, output]
    if debug:
        accordion = widgets.Accordion(children=[debugo], titles=("Debug",))
        items.append(accordion)

    vbox = widgets.VBox(items)

    # Display the text input widget
    display(vbox)


@contextmanager
def set_widget_logger(output: Optional[widgets.Output]) -> Iterator[logging.Logger]:
    if output is None:
        logger = NOOP_LOGGER
    else:
        logger = logging.getLogger("widget")
        logger.handlers.clear()
        logger.addHandler(_WidgetLogHandler(output))
        logger.propagate = False
        output.clear_output()
    token = _WIDGET_LOGGER.set(logger)
    try:
        yield logger
    finally:
        _WIDGET_LOGGER.reset(token)


def get_widget_logger() -> logging.Logger:
    return _WIDGET_LOGGER.get()


class _WidgetLogHandler(logging.Handler):
    def __init__(self, output: widgets.Output):
        super().__init__()
        self.output = output

    def emit(self, record: Any) -> None:
        with self.output:
            print(self.format(record))
