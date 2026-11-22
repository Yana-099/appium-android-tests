"""Проверки утилиты отправки Telegram-уведомлений."""

import importlib.util
from pathlib import Path


def load_telegram_report_module():
    """Загружает утилиту напрямую, не выполняя её точку входа."""
    script_path = Path(__file__).parents[2] / "tools" / "send_telegram_report.py"
    spec = importlib.util.spec_from_file_location("send_telegram_report", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_reads_russian_multiline_message_from_utf8_bom_file(tmp_path):
    """Утилита сохраняет кириллицу и переносы строк из файла PowerShell."""
    message = "Статус: ✅ Успешно\nНабор: smoke\nPassed: 4"
    message_file = tmp_path / "telegram-message.txt"
    message_file.write_bytes(b"\xef\xbb\xbf" + message.encode("utf-8"))

    telegram_report = load_telegram_report_module()

    assert telegram_report.read_message_from_file(message_file) == message
