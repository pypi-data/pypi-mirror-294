import importlib.metadata
from decimal import Decimal

from mm_std import utc_now
from pydantic import Field

from mm_base1.config import BaseAppConfig
from mm_base1.services.dconfig_service import DC, DConfigStorage
from mm_base1.services.dvalue_service import DV, DValueStorage


def _get_version() -> str:
    try:
        return importlib.metadata.version("app")
    except importlib.metadata.PackageNotFoundError:
        return " unknown"


class AppConfig(BaseAppConfig):
    app_version: str = _get_version()
    tags: list[str] = Field(["data"])
    main_menu: dict[str, str] = Field({"/data": "data"})
    telegram_bot_help: str = """
/first_command - bla bla1
/second_command - bla bla2
"""


class DConfigSettings(DConfigStorage):
    telegram_token = DC("", "telegram bot token", hide=True)
    telegram_chat_id = DC(0, "telegram chat id")
    telegram_polling = DC(False)
    telegram_admins = DC("", "admin1,admin2,admin3")
    price = DC(Decimal("1.23"), "long long long long long long long long long long long long long long long long ")
    secret_password = DC("abc", hide=True)
    long_cfg_1 = DC("many lines \n" * 5)


class DValueSettings(DValueStorage):
    tmp1 = DV("bla")
    tmp2 = DV("bla")
    processed_block = DV(111, "bla bla about processed_block")
    last_checked_at = DV(utc_now(), "bla bla about last_checked_at", False)
