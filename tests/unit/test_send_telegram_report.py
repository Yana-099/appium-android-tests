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


def test_builds_russian_multiline_summary_for_successful_test_run():
    """Утилита формирует понятную Telegram-сводку без участия PowerShell."""
    telegram_report = load_telegram_report_module()

    assert telegram_report.build_test_run_summary(
        outcome="success",
        test_scope="smoke",
        passed="4",
        failed="0",
        run_url="https://example.test/actions/runs/1",
    ) == (
        "Android UI tests\n"
        "Статус: ✅ Успешно\n"
        "Набор: smoke\n"
        "Passed: 4\n"
        "Failed: 0\n"
        "Запуск: https://example.test/actions/runs/1"
    )
