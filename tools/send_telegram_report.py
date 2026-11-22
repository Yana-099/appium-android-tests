"""Отправляет сообщение в Telegram через Bot API."""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_required_environment_variable(name: str) -> str:
    """Возвращает обязательную переменную окружения или завершает программу с ошибкой."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задана обязательная переменная окружения: {name}")
    return value


def read_message_from_file(message_file: Path) -> str:
    """Считывает текст уведомления из UTF-8-файла, созданного PowerShell."""
    return message_file.read_text(encoding="utf-8-sig")


def send_telegram_message(token: str, chat_id: str, message: str) -> None:
    """Отправляет текстовое сообщение в указанный Telegram-чат."""
    payload = json.dumps(
        {"chat_id": chat_id, "text": message, "disable_web_page_preview": True}
    ).encode("utf-8")
    request = Request(
        url=f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError(f"Telegram API вернул статус {response.status}")


def main() -> int:
    """Считывает параметры запуска и отправляет сообщение."""
    parser = argparse.ArgumentParser(description="Отправка сообщения в Telegram")
    message_source = parser.add_mutually_exclusive_group(required=True)
    message_source.add_argument("--message", help="Текст сообщения")
    message_source.add_argument(
        "--message-file",
        type=Path,
        help="Путь к UTF-8-файлу с текстом сообщения",
    )
    args = parser.parse_args()

    try:
        token = get_required_environment_variable("TELEGRAM_BOT_TOKEN")
        chat_id = get_required_environment_variable("TELEGRAM_CHAT_ID")
        message = args.message or read_message_from_file(args.message_file)
        send_telegram_message(token, chat_id, message)
    except (HTTPError, URLError, RuntimeError) as error:
        print(f"Не удалось отправить уведомление в Telegram: {error}", file=sys.stderr)
        return 1

    print("Уведомление отправлено в Telegram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
