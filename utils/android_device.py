import os
import re
import shlex
import subprocess
from pathlib import Path


MAX_FAILURE_LOGCAT_LINES = 80

class AndroidDeviceCommandError(RuntimeError):
    pass


def _adb_environment() -> dict[str, str]:
    environment = os.environ.copy()
    user_profile = environment.get("USERPROFILE")
    if not user_profile:
        home_drive = environment.get("HOMEDRIVE")
        home_path = environment.get("HOMEPATH")
        user_profile = f"{home_drive}{home_path}" if home_drive and home_path else str(Path.home())

    environment["HOME"] = user_profile
    environment["USERPROFILE"] = user_profile
    environment["ANDROID_USER_HOME"] = str(Path(user_profile) / ".android")
    return environment


def post_test_notification(udid: str, title: str, text: str):
    notification_command = " ".join(
        [
            "cmd",
            "notification",
            "post",
            "-S",
            "bigtext",
            "-t",
            shlex.quote(title),
            "lifecycle-test",
            shlex.quote(text),
        ]
    )

    try:
        subprocess.run(
            [
                "adb",
                "-s",
                udid,
                "shell",
                notification_command,
            ],
            check=True,
            capture_output=True,
            text=True,
            env=_adb_environment(),
        )
    except subprocess.CalledProcessError as error:
        command_output = (error.stderr or error.stdout).strip()
        error_message = (
            "Не удалось отправить тестовое уведомление через ADB. "
            "Проверьте доступность эмулятора и ADB."
        )
        if command_output:
            error_message = f"{error_message} Ответ ADB: {command_output}"
        raise AndroidDeviceCommandError(error_message) from error


def crash_application(udid: str, app_package: str):
    try:
        subprocess.run(
            ["adb", "-s", udid, "shell", "am", "crash", app_package],
            check=True,
            capture_output=True,
            text=True,
            env=_adb_environment(),
        )
    except subprocess.CalledProcessError as error:
        command_output = (error.stderr or error.stdout).strip()
        error_message = (
            "Не удалось принудительно завершить приложение через ADB. "
            "Проверьте доступность эмулятора и ADB."
        )
        if command_output:
            error_message = f"{error_message} Ответ ADB: {command_output}"
        raise AndroidDeviceCommandError(error_message) from error


def collapse_notification_shade(udid: str):
    try:
        subprocess.run(
            ["adb", "-s", udid, "shell", "cmd", "statusbar", "collapse"],
                check=True,
                capture_output=True,
                text=True,
                env=_adb_environment(),
        )
    except subprocess.CalledProcessError as error:
        command_output = (error.stderr or error.stdout).strip()
        error_message = (
            "Не удалось закрыть шторку уведомлений через ADB. "
            "Проверьте доступность эмулятора и ADB."
        )
        if command_output:
            error_message = f"{error_message} Ответ ADB: {command_output}"
        raise AndroidDeviceCommandError(error_message) from error


def get_logcat(udid: str, lines: int = 500) -> str:
    try:
        completed_process = subprocess.run(
            ["adb", "-s", udid, "logcat", "-d", "-t", str(lines)],
            check=True,
            capture_output=True,
            text=True,
            errors="replace",
            env=_adb_environment(),
        )
    except subprocess.CalledProcessError as error:
        command_output = (error.stderr or error.stdout).strip()
        error_message = (
            "Не удалось получить Android logcat через ADB. "
            "Проверьте доступность эмулятора и ADB."
        )
        if command_output:
            error_message = f"{error_message} Ответ ADB: {command_output}"
        raise AndroidDeviceCommandError(error_message) from error
    return completed_process.stdout


def filter_failure_logcat(
    logcat: str, app_package: str, max_lines: int = MAX_FAILURE_LOGCAT_LINES
) -> str:
    """Оставляет строки уровня E/F, относящиеся к тестируемому приложению."""
    relevant_lines = [
        line
        for line in logcat.splitlines()
        if app_package in line and re.search(r"(?:^|\s)[EF]\s+[^:\s]+:", line)
    ]
    if not relevant_lines:
        return "В Android logcat не найдены релевантные ошибки приложения."
    return "\n".join(relevant_lines[-max_lines:])


def get_failure_logcat(udid: str, app_package: str, lines: int = 500) -> str:
    return filter_failure_logcat(get_logcat(udid, lines), app_package)


def get_crash_logcat(udid: str, app_package: str, lines: int = 1000) -> str:
    logcat_lines = get_logcat(udid, lines).splitlines()

    for index in range(len(logcat_lines) - 1, -1, -1):
        if "FATAL EXCEPTION" not in logcat_lines[index]:
            continue

        exception_block = [logcat_lines[index]]
        for line in logcat_lines[index + 1 :]:
            if " AndroidRuntime:" not in line:
                break
            exception_block.append(line)

        if any(app_package in line for line in exception_block):
            return "\n".join(exception_block)

    return (
        f"В Android logcat не найден блок FATAL EXCEPTION для приложения {app_package}.\n"
        "Для обычных упавших тестов сохраняется только релевантный фрагмент logcat."
    )
