import json
from pathlib import Path


def remove_internal_fixture_steps(results_dir: Path) -> None:
    for container_path in results_dir.glob("*-container.json"):
        container = json.loads(container_path.read_text(encoding="utf-8"))
        afters = container.get("afters", [])
        visible_afters = [
            after for after in afters if not after.get("name", "").endswith("::<lambda>")
        ]
        if len(visible_afters) != len(afters):
            container["afters"] = visible_afters
            container_path.write_text(
                json.dumps(container, ensure_ascii=False), encoding="utf-8"
            )
