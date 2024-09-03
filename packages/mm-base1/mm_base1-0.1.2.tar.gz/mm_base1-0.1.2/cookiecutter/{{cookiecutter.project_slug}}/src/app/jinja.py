from markupsafe import Markup
from mm_base1.jinja import CustomJinja

from app.app import App


def header_info(_app: App) -> Markup:
    info = ""
    return Markup(info)


custom_jinja = CustomJinja(header_info=header_info)
