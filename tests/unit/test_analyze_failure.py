"""Проверки demo-скрипта AI-анализа одного упавшего Allure-теста."""

import importlib.util
import json
from pathlib import Path


def load_analyze_failure_module():
    script_path = Path(__file__).parents[2] / "tools" / "analyze_failure.py"
    spec = importlib.util.spec_from_file_location("analyze_failure", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_failed_result(results_dir: Path) -> None:
    (results_dir / "screen.png").write_bytes(b"not-needed-without-key")
    (results_dir / "source.xml").write_text(
        """
        <hierarchy>
          <android.widget.TextView resource-id="app:id/loginTV" text="Login" bounds="[1,1][20,20]" />
          <android.view.View clickable="false" bounds="[0,0][0,0]" />
        </hierarchy>
        """,
        encoding="utf-8",
    )
    (results_dir / "logcat.txt").write_text(
        "E AndroidRuntime: useful failure\nBearer very-secret-token\n",
        encoding="utf-8",
    )
    (results_dir / "failed-result.json").write_text(
        json.dumps(
            {
                "uuid": "failed-test-uuid",
                "name": "Пользователь видит ошибку при неверном пароле",
                "status": "failed",
                "start": 2,
                "statusDetails": {
                    "message": "AssertionError: expected Login",
                    "trace": "tests/login/test_invalid_authorization.py:33",
                },
                "attachments": [
                    {"name": "Screenshot", "type": "image/png", "source": "screen.png"},
                    {"name": "Page source", "type": "application/xml", "source": "source.xml"},
                    {"name": "Logcat", "type": "text/plain", "source": "logcat.txt"},
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_compacts_xml_to_meaningful_visible_nodes():
    analyze_failure = load_analyze_failure_module()

    compact_xml = analyze_failure.compact_xml(
        """
        <hierarchy>
          <android.widget.TextView resource-id="app:id/loginTV" text="Login" bounds="[1,1][20,20]" />
          <android.view.View clickable="false" bounds="[0,0][0,0]" />
        </hierarchy>
        """
    )

    assert 'id="app:id/loginTV"' in compact_xml
    assert 'text="Login"' in compact_xml
    assert "android.view.View" not in compact_xml


def test_redacts_quoted_password_and_token_values():
    analyze_failure = load_analyze_failure_module()
    source = (
        'password: "secret-one"; token=\'secret-two\'; '
        '{"password":"secret-three"}; '
        '<node password="secret-four" />; '
        "https://example.test/?api_key=secret-five"
    )

    redacted = analyze_failure.redact(source)

    assert "secret-" not in redacted
    assert redacted.count("[REDACTED]") == 5


def test_openai_request_disables_storage_and_uses_strict_schema():
    analyze_failure = load_analyze_failure_module()

    request_body = analyze_failure.build_request_body("safe context", None)

    assert request_body["store"] is False
    assert request_body["text"]["format"]["strict"] is True
    assert request_body["text"]["format"]["schema"]["additionalProperties"] is False


def test_without_api_key_writes_human_readable_report_and_returns_zero(
    tmp_path, monkeypatch
):
    analyze_failure = load_analyze_failure_module()
    results_dir = tmp_path / "allure-results"
    results_dir.mkdir()
    write_failed_result(results_dir)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    exit_code = analyze_failure.main(["--results", str(results_dir)])

    report_path = tmp_path / "artifacts" / "ai-report.md"
    assert exit_code == 0
    assert report_path.exists()
    assert "AI-анализ не выполнен: не задан OPENAI_API_KEY" in report_path.read_text(
        encoding="utf-8"
    )


def test_adds_markdown_analysis_as_attachment_to_the_same_allure_result(tmp_path):
    analyze_failure = load_analyze_failure_module()
    results_dir = tmp_path / "allure-results"
    results_dir.mkdir()
    write_failed_result(results_dir)
    result_path = results_dir / "failed-result.json"
    report = "# AI-анализ падения\n\n## Root cause\nОткрыт не тот экран.\n"

    analyze_failure.attach_report_to_allure(results_dir, result_path, report)

    result = json.loads(result_path.read_text(encoding="utf-8"))
    attachment = next(
        item
        for item in result["attachments"]
        if item["name"] == "AI failure analysis"
    )
    assert attachment["type"] == "text/markdown"
    assert (results_dir / attachment["source"]).read_text(encoding="utf-8") == report
