"""Показывает AI-анализ одного последнего упавшего Allure-теста."""

import argparse
import base64
import json
import os
import re
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4o-mini"
MAX_LOGCAT_CHARS = 4_000
MAX_TRACE_CHARS = 3_000


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI-анализ последнего failed/broken Allure result."
    )
    parser.add_argument(
        "--results",
        type=Path,
        required=True,
        help="Путь к каталогу allure-results.",
    )
    parser.add_argument(
        "--include-screenshot",
        action="store_true",
        default=True,
        help="Передать screenshot модели (в demo включено по умолчанию).",
    )
    parser.add_argument(
        "--no-screenshot",
        action="store_false",
        dest="include_screenshot",
        help="Не передавать screenshot модели.",
    )
    return parser.parse_args(argv)


def redact(text: str) -> str:
    """Маскирует наиболее частые секретоподобные фрагменты в тексте."""
    text = re.sub(r"(?i)(bearer\s+)[^\s]+", r"\1[REDACTED]", text)
    return re.sub(
        r"(?i)((?:[\"']?)(?:password|token|api[_-]?key|authorization)(?:[\"']?)\s*[=:]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s,;>&]+)",
        r"\1[REDACTED]",
        text,
    )


def has_non_zero_bounds(bounds: str) -> bool:
    values = [int(value) for value in re.findall(r"-?\d+", bounds)]
    return len(values) == 4 and values[0] != values[2] and values[1] != values[3]


def compact_xml(xml_source: str) -> str:
    """Оставляет из page source только видимые или информативные UI-узлы."""
    try:
        root = ElementTree.fromstring(xml_source)
    except ElementTree.ParseError:
        return "XML page source не удалось разобрать."

    lines: list[str] = []
    for node in root.iter():
        if node is root:
            continue
        attributes = node.attrib
        bounds = attributes.get("bounds", "")
        meaningful = any(
            attributes.get(name)
            for name in ("resource-id", "text", "content-desc", "name", "label")
        )
        clickable = attributes.get("clickable") == "true"
        if not meaningful and not clickable and not has_non_zero_bounds(bounds):
            continue

        details = []
        for source, label in (
            ("resource-id", "id"),
            ("text", "text"),
            ("content-desc", "content-desc"),
            ("name", "name"),
            ("label", "label"),
            ("enabled", "enabled"),
            ("clickable", "clickable"),
            ("bounds", "bounds"),
        ):
            if attributes.get(source):
                details.append(f'{label}="{redact(attributes[source])}"')
        lines.append(f"[{node.tag}] {' '.join(details)}")

    return "\n".join(lines) or "В XML нет значимых UI-узлов."


def read_allure_result(results_dir: Path) -> tuple[dict[str, Any], Path] | None:
    candidates: list[tuple[int, dict[str, Any], Path]] = []
    for result_path in results_dir.glob("*-result.json"):
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if result.get("status") not in {"failed", "broken"}:
            continue
        try:
            start_time = int(result.get("start", 0))
        except (TypeError, ValueError):
            start_time = 0
        candidates.append((start_time, result, result_path))

    if not candidates:
        return None
    _, result, result_path = max(candidates, key=lambda candidate: candidate[0])
    return result, result_path


def attachment_path(results_dir: Path, result: dict[str, Any], kind: str) -> Path | None:
    for attachment in result.get("attachments", []):
        attachment_type = attachment.get("type", "")
        attachment_name = attachment.get("name", "").lower()
        source = attachment.get("source")
        if not source:
            continue
        matches = {
            "screenshot": attachment_type.startswith("image/"),
            "xml": attachment_type in {"application/xml", "text/xml"} or str(source).endswith(".xml"),
            "logcat": "logcat" in attachment_name,
        }
        if not matches.get(kind):
            continue
        path = (results_dir / source).resolve()
        if path.is_relative_to(results_dir.resolve()) and path.is_file():
            return path
    return None


def build_context(results_dir: Path, result: dict[str, Any]) -> tuple[str, Path | None]:
    details = result.get("statusDetails", {})
    xml_path = attachment_path(results_dir, result, "xml")
    logcat_path = attachment_path(results_dir, result, "logcat")
    screenshot_path = attachment_path(results_dir, result, "screenshot")
    compact_source = (
        compact_xml(xml_path.read_text(encoding="utf-8", errors="replace"))
        if xml_path
        else "XML attachment не найден."
    )
    logcat = (
        redact(logcat_path.read_text(encoding="utf-8", errors="replace"))[:MAX_LOGCAT_CHARS]
        if logcat_path
        else "Logcat attachment не найден."
    )
    trace = redact(str(details.get("trace", "")))[:MAX_TRACE_CHARS]
    context = "\n\n".join(
        [
            f"Тест: {result.get('name', 'без названия')}",
            f"Ошибка pytest: {redact(str(details.get('message', 'не указана')))}",
            f"Traceback:\n{trace or 'не указан'}",
            f"Сжатый XML:\n{compact_source}",
            f"Logcat (фрагмент):\n{logcat}",
        ]
    )
    return context, screenshot_path


def response_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "root_cause": {"type": "string"},
            "evidence": {"type": "string"},
            "suggested_fix": {"type": "string"},
        },
        "required": ["root_cause", "evidence", "suggested_fix"],
        "additionalProperties": False,
    }


def build_request_body(context: str, screenshot_path: Path | None) -> dict[str, Any]:
    content: list[dict[str, Any]] = [
        {
            "type": "input_text",
            "text": (
                "Ты QA-инженер. Проанализируй один сбой мобильного UI-теста. "
                "Отвечай по-русски, коротко и только на основе доказательств. "
                "Не утверждай, что locator сломан, если XML и screenshot показывают иной экран.\n\n"
                f"{context}"
            ),
        }
    ]
    if screenshot_path:
        encoded_image = base64.b64encode(screenshot_path.read_bytes()).decode("ascii")
        content.append(
            {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{encoded_image}",
                "detail": "low",
            }
        )

    return {
        "model": os.getenv("AI_FAILURE_MODEL", DEFAULT_MODEL),
        "store": False,
        "input": [{"role": "user", "content": content}],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "mobile_failure_analysis",
                "strict": True,
                "schema": response_schema(),
            }
        },
    }


def extract_output_text(response: dict[str, Any]) -> str:
    if response.get("output_text"):
        return str(response["output_text"])
    for output_item in response.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") == "output_text":
                return str(content_item.get("text", ""))
    raise ValueError("Ответ API не содержит текстового Structured Output.")


def request_analysis(api_key: str, body: dict[str, Any]) -> dict[str, str]:
    request = Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:  # nosec B310: fixed OpenAI HTTPS endpoint
        payload = json.loads(response.read().decode("utf-8"))
    analysis = json.loads(extract_output_text(payload))
    required_fields = {"root_cause", "evidence", "suggested_fix"}
    if set(analysis) != required_fields or not all(
        isinstance(analysis[field], str) for field in required_fields
    ):
        raise ValueError("Ответ API не соответствует ожидаемой схеме.")
    return analysis


def render_report(test_name: str, analysis: dict[str, str] | None, message: str) -> str:
    lines = ["# AI-анализ падения", "", f"**Тест:** {test_name}", ""]
    if analysis is None:
        return "\n".join(lines + [message, ""])
    return "\n".join(
        lines
        + [
            "## Root cause",
            analysis["root_cause"],
            "",
            "## Evidence",
            analysis["evidence"],
            "",
            "## Suggested fix",
            analysis["suggested_fix"],
            "",
        ]
    )


def write_report(results_dir: Path, report: str) -> Path:
    report_path = results_dir.parent / "artifacts" / "ai-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def attach_report_to_allure(results_dir: Path, result_path: Path, report: str) -> Path:
    """Добавляет Markdown-отчёт к исходному failed/broken результату Allure."""
    result = json.loads(result_path.read_text(encoding="utf-8"))
    raw_uuid = str(result.get("uuid", result_path.stem))
    safe_uuid = re.sub(r"[^A-Za-z0-9_.-]", "_", raw_uuid)
    source = f"ai-failure-analysis-{safe_uuid}.md"
    attachment_path = results_dir / source
    attachment_path.write_text(report, encoding="utf-8")

    attachments = result.get("attachments", [])
    result["attachments"] = [
        attachment
        for attachment in attachments
        if attachment.get("name") != "AI failure analysis"
    ]
    result["attachments"].append(
        {
            "name": "AI failure analysis",
            "type": "text/markdown",
            "source": source,
        }
    )
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return attachment_path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    found_result = read_allure_result(args.results)
    if found_result is None:
        print("AI-анализ не выполнен: failed/broken Allure result не найден.")
        return 0

    result, result_path = found_result
    test_name = str(result.get("name", "без названия"))
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        report = render_report(
            test_name, None, "AI-анализ не выполнен: не задан OPENAI_API_KEY."
        )
        report_path = write_report(args.results, report)
        attachment_path = attach_report_to_allure(args.results, result_path, report)
        print(
            f"{report}\nОтчёт сохранён: {report_path}\n"
            f"Вложение Allure добавлено: {attachment_path}"
        )
        return 0

    try:
        context, screenshot_path = build_context(args.results, result)
        if not args.include_screenshot:
            screenshot_path = None
        analysis = request_analysis(api_key, build_request_body(context, screenshot_path))
        report = render_report(test_name, analysis, "")
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        report = render_report(
            test_name,
            None,
            "AI-анализ не выполнен: ошибка сети, API или формата ответа.",
        )

    report_path = write_report(args.results, report)
    attachment_path = attach_report_to_allure(args.results, result_path, report)
    print(
        f"{report}\nОтчёт сохранён: {report_path}\n"
        f"Вложение Allure добавлено: {attachment_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
