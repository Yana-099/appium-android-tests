import json
import sys
from urllib.parse import parse_qs, urlparse

import pytest

from tools import generate_from_qase


@pytest.fixture
def generator():
    return generate_from_qase


def test_fetches_one_planned_case(generator, monkeypatch):
    def fake_request(request):
        url = urlparse(request.full_url)
        assert url.netloc == "api.qase.io"
        assert url.path == "/v1/case/AMT"
        assert parse_qs(url.query) == {
            "automation": ["to-be-automated"],
            "limit": ["1"],
        }
        return {"result": {"entities": [{"id": 15}]}}

    monkeypatch.setattr(generator, "request_json", fake_request)
    assert generator.fetch_case("AMT", None, "placeholder") == {"id": 15}


def test_reads_only_public_constant_names(generator, monkeypatch, tmp_path):
    config = tmp_path / "config"
    config.mkdir()
    (config / "test_data.py").write_text(
        'CITY = "demo"\nZIP_CODE: str = "12345"\n_PRIVATE = "hidden"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(generator, "ROOT", tmp_path)
    assert generator.test_data_names() == ["CITY", "ZIP_CODE"]


@pytest.mark.parametrize("statement", [
    "time.sleep(1)",
    "from time import sleep as pause; pause(1)",
    "driver.find_element(locator)",
    "driver.find_elements(locator)",
])
def test_rejects_direct_calls(generator, statement):
    code = f"@qase.id(15)\n@pytest.mark.ai_generated\ndef test_case():\n    {statement}"
    with pytest.raises(ValueError, match="Use Page Object"):
        generator.validate(code, 15)


@pytest.mark.parametrize(
    ("response", "exit_code"),
    [
        ({"code": "@qase.id(15)\n@pytest.mark.ai_generated\ndef test_case(): pass"}, 0),
        ({"missing_methods": ["Read product prices"]}, 2),
        ({"code": "# @qase.id(15)\n@pytest.mark.ai_generated\ndef test_case(): pass"}, 1),
    ],
)
def test_offline_draft(generator, tmp_path, monkeypatch, response, exit_code):
    case_path = tmp_path / "case.json"
    case_path.write_text(json.dumps({"id": 15}), encoding="utf-8")
    response_path = tmp_path / "response.json"
    response_path.write_text(json.dumps(response), encoding="utf-8")
    monkeypatch.setattr(generator, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "generate_from_qase", "--mock-case", str(case_path),
        "--mock-response", str(response_path),
    ])
    draft = tmp_path / "artifacts/qase-generated/test_amt_15.py"
    if exit_code == 1:
        with pytest.raises(SystemExit) as error:
            generator.main()
        assert error.value.code == 1
    else:
        assert generator.main() == exit_code
    assert draft.exists() == (exit_code == 0)
    if draft.exists():
        original = draft.read_bytes()
        with pytest.raises(SystemExit) as error:
            generator.main()
        assert error.value.code == 1
        assert draft.read_bytes() == original
