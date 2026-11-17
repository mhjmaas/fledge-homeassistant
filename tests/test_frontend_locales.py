"""The panel's and the schedule cards' message catalogs (frontend/locales):
every language as complete as English, with English's placeholders, and
English holding exactly the messages the scripts use."""

import json
import re
from pathlib import Path

import pytest

FRONTEND = Path(__file__).parent.parent / "custom_components" / "fledge" / "frontend"
LOCALES = FRONTEND / "locales"
SCRIPTS = [FRONTEND / "fledge-panel.js", FRONTEND / "fledge-schedule-card.js"]


def catalog(code: str) -> dict[str, str]:
    return json.loads((LOCALES / f"{code}.json").read_text(encoding="utf-8"))


def placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


def source() -> str:
    return "\n".join(script.read_text(encoding="utf-8") for script in SCRIPTS)


LANGUAGES = sorted(p.stem for p in LOCALES.glob("*.json"))
OTHERS = [code for code in LANGUAGES if code != "en"]


def test_the_helper_offers_every_catalog() -> None:
    helper = (FRONTEND / "fledge-i18n.js").read_text(encoding="utf-8")
    offered = re.search(r"const LANGUAGES = \[([^\]]*)\]", helper).group(1)
    assert sorted(re.findall(r'"(\w+)"', offered)) == LANGUAGES


@pytest.mark.parametrize("code", OTHERS)
def test_a_catalog_has_every_message_and_its_placeholders(code: str) -> None:
    english, other = catalog("en"), catalog(code)
    assert sorted(set(english) - set(other)) == [], "missing"
    assert sorted(set(other) - set(english)) == [], "not in English"
    assert [key for key, text in other.items() if not text.strip()] == [], "empty"
    assert [key for key in english if placeholders(english[key]) != placeholders(other[key])] == [], "placeholders differ"


def test_every_message_the_scripts_ask_for_is_in_english() -> None:
    asked = set(re.findall(r"""\b(?:tr|tn|has)\(\s*["'`]([^"'`$]+)["'`]""", source()))
    assert sorted(asked - set(catalog("en"))) == []


def test_every_english_message_is_used() -> None:
    code = source()
    quoted = set(re.findall(r"""["'`]([a-z_][\w.-]*\.[\w.-]+)["'`]""", code))
    # Messages looked up by value: `layout.${k}`, `screen.weather.${c}`.
    prefixes = set(re.findall(r"`([a-z_][\w.]*\.)\$\{", code))

    def used(key: str) -> bool:
        whole = re.sub(r"_(one|sub)$", "", key)
        return key in quoted or whole in quoted or any(key.startswith(p) for p in prefixes)

    assert sorted(key for key in catalog("en") if not used(key)) == []
