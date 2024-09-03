from mm_base1.telegram import BaseTelegram
from telebot.types import Message


class Telegram(BaseTelegram):
    def init_commands(self) -> None:
        @self.bot.message_handler(commands=["ping2"])  # type: ignore
        @self.auth(admins=self.admins, bot=self.bot)
        def ping_handler(message: Message) -> None:
            text = message.text.replace("/ping2", "").strip()
            self._send_message(message.chat.id, f"pong pong {text}")
