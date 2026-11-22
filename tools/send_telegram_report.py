"""Отправляет сообщение в Telegram через Bot API."""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_required_environment_variable(name: str) -> str:
    """Возвращает обязательную переменную окружения или завершает программу с ошибкой."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Не задана обязательная переменная окружения: {name}")
    return value


def build_test_run_summary(
    outcome: str,
    test_scope: str,
    passed: str,
    failed: str,
    run_url: str,
) -> str:
    """Формирует русскоязычную сводку о прогоне UI-тестов."""
    status = "✅ Успешно" if outcome == "success" else "❌ Есть ошибки"
    return "\n".join(
        (
            "Android UI tests",
            f"Статус: {status}",
            f"Набор: {test_scope}",
            f"Passed: {passed}",
            f"Failed: {failed}",
            f"Запуск: {run_url}",
        )
    )


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
    message_source.add_argument("--test-run-summary", action="store_true")
    parser.add_argument("--test-outcome", help="Результат прогона pytest")
    parser.add_argument("--test-scope", help="Маркер запущенной группы тестов")
    parser.add_argument("--passed", help="Количество успешных тестов")
    parser.add_argument("--failed", help="Количество упавших тестов")
    parser.add_argument("--run-url", help="Ссылка на запуск GitHub Actions")
    args = parser.parse_args()

    try:
        token = get_required_environment_variable("TELEGRAM_BOT_TOKEN")
        chat_id = get_required_environment_variable("TELEGRAM_CHAT_ID")
        if args.test_run_summary:
            summary_arguments = (
                args.test_outcome,
                args.test_scope,
                args.passed,
                args.failed,
                args.run_url,
            )
            if not all(summary_arguments):
                raise RuntimeError("Не заданы данные для сводки о прогоне тестов")
            message = build_test_run_summary(*summary_arguments)
        else:
            message = args.message
        send_telegram_message(token, chat_id, message)
    except (HTTPError, URLError, RuntimeError) as error:
        print(f"Не удалось отправить уведомление в Telegram: {error}", file=sys.stderr)
        return 1

    print("Уведомление отправлено в Telegram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
