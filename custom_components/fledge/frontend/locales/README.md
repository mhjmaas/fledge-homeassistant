# The panel's and schedule cards' message catalogs

`en.json` holds every word the Fledge panel (`fledge-panel.js`) and the
schedule cards (`fledge-schedule-card.js`) show. Every other file holds one
language, named by its code (`nl.json`), with the same message IDs. Each
viewer sees their own Home Assistant language (their profile's), where it has
a catalog. A catalog answers a language's first part (`nl` serves `nl-BE`).
A message missing from a catalog is shown in English.

The scripts look messages up with `fledge-i18n.js`: `tr("message.id")`, or
`tr("message.id", { name: value })` for one with a `{name}` in it. Values are
filled in by name, so a translation can put them in its own order.
`tn("message.id", count)` uses `message.id_one` when there is one of
something. A message ending in `_sub` is the line under the message without
it.

## The Nest's screen

`screen.*` messages are what the Nest's own screen says, which the panel's
preview draws. Each is nestlocal's message of the same ID after `screen.`, in
nestlocal's words (`crates/nestlocal/locales` in the Fledge repository).
Change them there first, then copy them here, so the preview says exactly
what the Nest does.

## Adding a language

1. **Copy `en.json`** to a file named with the language's code, `de.json` for
   German.
2. **Translate the values.** Keep the message IDs and every `{placeholder}`.
   A `<b>…</b>` stays around the word it makes bold. Copy each `screen.*`
   message from nestlocal's catalog for the language, rather than translating
   it again.
3. **Add the code to `LANGUAGES`** in `../fledge-i18n.js`.
4. **Check it**: `pytest tests/test_frontend_locales.py` fails on a missing,
   extra or empty message, a placeholder that no longer matches English's,
   and an English message no script uses, or a script's message English
   lacks.

The integration's own setup, options, entity names and services are
translated by Home Assistant itself, from `../../translations/<code>.json`.
