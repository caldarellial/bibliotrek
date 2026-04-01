import i18n from "i18next";
import { initReactI18next } from "react-i18next";

/**
 * Loads every `locales/<languageCode>/<namespace>.json` file at bundle time via
 * Metro `require.context` (requires `unstable_allowRequireContext` in metro.config.js).
 * Nested paths under a language folder are ignored.
 */
type LocaleResources = Record<string, Record<string, object>>;

type MetroRequireContext = {
  <T = object>(id: string): T;
  keys(): string[];
};

function buildLocaleResources(): {
  resources: LocaleResources;
  languageCodes: string[];
  namespaces: string[];
} {
  const ctx = (
    require as unknown as {
      context(
        path: string,
        deep?: boolean,
        filter?: RegExp,
      ): MetroRequireContext;
    }
  ).context("../locales", true, /\.json$/);

  const resources: LocaleResources = {};
  const namespaceSet = new Set<string>();

  for (const key of ctx.keys()) {
    const match = key.match(/^\.\/([^/]+)\/([^/]+)\.json$/);
    if (!match) continue;
    const [, languageCode, namespace] = match;
    if (!resources[languageCode]) resources[languageCode] = {};
    resources[languageCode][namespace] = ctx(key);
    namespaceSet.add(namespace);
  }

  const languageCodes = Object.keys(resources).sort();
  const namespaces = Array.from(namespaceSet).sort();

  return { resources, languageCodes, namespaces };
}

const { resources, languageCodes, namespaces } = buildLocaleResources();

if (languageCodes.length === 0) {
  throw new Error(
    "i18n: add at least one file at locales/<languageCode>/<namespace>.json",
  );
}

function pickInitialLng(codes: string[]): string {
  if (codes.includes("en")) return "en";
  return codes[0];
}

function pickFallbackLng(codes: string[]): string {
  if (codes.includes("en")) return "en";
  return codes[0];
}

function pickDefaultNs(lng: string, nsSorted: string[]): string {
  const forLang = resources[lng];
  if (forLang && "common" in forLang) return "common";
  const keys = forLang ? Object.keys(forLang).sort() : [];
  return keys[0] ?? nsSorted[0] ?? "translation";
}

const lng = pickInitialLng(languageCodes);
const fallbackLng = pickFallbackLng(languageCodes);
export const defaultNS = pickDefaultNs(lng, namespaces);

export { languageCodes, resources };

void i18n.use(initReactI18next).init({
  resources,
  lng,
  fallbackLng,
  defaultNS,
  ns: namespaces,
  interpolation: {
    escapeValue: false,
  },
  react: {
    useSuspense: false,
  },
});

export default i18n;
