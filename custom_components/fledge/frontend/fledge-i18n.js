// The panel's and the schedule cards' words in the viewer's own Home
// Assistant language, from locales/<language>.json beside this file. A
// catalog answers a language's first part (nl serves nl-BE), and a message
// it lacks is shown in English. Messages are named by ID; a {name} in one
// is filled in by name, so a translation can put them in its own order.
// locales/README.md says how to add a language.

const LANGUAGES = ["en", "nl"];
// This module's own address, version and all, so a new release's catalogs
// aren't an old one's from the browser's cache.
const HERE = new URL(import.meta.url);
const loaded = {};
let current = "en";

async function fill(code) {
  if (loaded[code]) return;
  try {
    const answer = await fetch(new URL(`locales/${code}.json${HERE.search}`, HERE));
    loaded[code] = answer.ok ? await answer.json() : {};
  } catch (_) {
    loaded[code] = {};
  }
}

// The catalog's language for a viewer: theirs where there is one, else English.
export function languageOf(hass) {
  const said = String(hass?.locale?.language || hass?.language || document.documentElement.lang || "en");
  const code = said.toLowerCase().split(/[-_]/)[0];
  return LANGUAGES.includes(code) ? code : "en";
}

// The language t() speaks now.
export function language() {
  return current;
}

// Speaks the viewer's language from now on, once its catalog has come:
// true if that changed what t() says.
export async function use(hass) {
  const code = languageOf(hass);
  await Promise.all([fill("en"), fill(code)]);
  const changed = code !== current;
  current = code;
  return changed;
}

export function has(key) {
  return key in (loaded[current] || {}) || key in (loaded.en || {});
}

// A message, its {name}s filled in from `values`. A value is put in as it
// is, its own braces left alone; a {name} without one stays as written.
export function t(key, values = {}) {
  const text = loaded[current]?.[key] ?? loaded.en?.[key] ?? key;
  return text.replace(/\{(\w+)\}/g, (all, name) => (name in values ? String(values[name]) : all));
}

// A message that counts: `key`_one for one of them, where it has one.
export function tn(key, count, values = {}) {
  return t(count === 1 && has(`${key}_one`) ? `${key}_one` : key, { count, ...values });
}

// The page's own language until a viewer's comes, so the first drawing
// already speaks it.
await use(null);
