from typing import Any, TypeAlias
from collections.abc import Callable


def message_handler(
        commands: list[str] | None = None,
        regexp: str | None = None,
        func: Callable[..., Any] | None = None,
        content_types: list[str] | None = None,
        chat_types: list[str] | None = None,
        **kwargs: object,
) -> Callable[..., Any]: ...


TeleBot: TypeAlias = Any
