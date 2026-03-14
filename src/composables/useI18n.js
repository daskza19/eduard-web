import { ref, computed } from 'vue'
import manifest from '../assets/text/manifest.json'

const LANGUAGES = ['catalan', 'spanish', 'english']
const LANG_LABELS = { catalan: 'CAT', spanish: 'ESP', english: 'ENG' }
const DEFAULT_LANG = 'catalan'

const currentLang = ref(localStorage.getItem('lang') || DEFAULT_LANG)

// Build a lookup map: key -> { catalan, spanish, english }
const translations = {}
for (const entry of manifest) {
  translations[entry.key] = entry.traductions[0]
}

function setLang(lang) {
  if (LANGUAGES.includes(lang)) {
    currentLang.value = lang
    localStorage.setItem('lang', lang)
  }
}

function t(key) {
  const entry = translations[key]
  if (!entry) return key
  return entry[currentLang.value] || entry[DEFAULT_LANG] || key
}

export function useI18n() {
  return {
    currentLang,
    LANGUAGES,
    LANG_LABELS,
    setLang,
    t,
    translations,
  }
}
