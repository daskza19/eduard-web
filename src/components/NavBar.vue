<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from '../composables/useI18n.js'
import { vTextId } from '../directives/textId.js'

const { currentLang, LANGUAGES, LANG_LABELS, setLang } = useI18n()

const visible = ref(false)
const activeSection = ref('projects')

const sections = ['projects', 'info', 'chronology', 'contact']

function onScroll() {
  visible.value = window.scrollY > window.innerHeight * 0.8

  let current = sections[0]
  for (const id of sections) {
    const el = document.getElementById(id)
    if (el && el.getBoundingClientRect().top <= window.innerHeight * 0.4) {
      current = id
    }
  }
  activeSection.value = current
}

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <nav class="navbar" :class="{ visible }">
    <div class="nav-inner">
      <div class="nav-links">
        <a class="nav-link" :class="{ active: activeSection === 'projects' }" @click="scrollTo('projects')" v-text-id="'projects_title'"></a>
        <a class="nav-link" :class="{ active: activeSection === 'info' }" @click="scrollTo('info')" v-text-id="'info_title'"></a>
        <a class="nav-link" :class="{ active: activeSection === 'chronology' }" @click="scrollTo('chronology')" v-text-id="'chronology_title'"></a>
        <a class="nav-link" :class="{ active: activeSection === 'contact' }" @click="scrollTo('contact')" v-text-id="'contact_title'"></a>
      </div>

      <div class="lang-selector">
        <button
          v-for="lang in LANGUAGES"
          :key="lang"
          class="lang-btn"
          :class="{ active: currentLang === lang }"
          @click="setLang(lang)"
        >
          {{ LANG_LABELS[lang] }}
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(60, 60, 60, 0.8);
  transform: translateY(-100%);
  opacity: 0;
  transition: transform 0.4s ease, opacity 0.4s ease;
}

.navbar.visible {
  transform: translateY(0);
  opacity: 1;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  padding: 1rem 2rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.35);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  cursor: pointer;
  transition: color 0.3s, font-size 0.3s;
  user-select: none;
  white-space: nowrap;
}

.nav-link:hover {
  color: rgba(255, 255, 255, 0.6);
}

.nav-link.active {
  color: rgba(255, 255, 255, 0.85);
  font-weight: 700;
}

/* ── Language selector ── */
.lang-selector {
  display: flex;
  gap: 0.25rem;
  margin-left: 2rem;
  border-left: 1px solid rgba(255, 255, 255, 0.15);
  padding-left: 1.5rem;
}

.lang-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  cursor: pointer;
  padding: 0.25rem 0.4rem;
  transition: color 0.3s;
  user-select: none;
}

.lang-btn:hover {
  color: rgba(255, 255, 255, 0.6);
}

.lang-btn.active {
  color: rgba(255, 255, 255, 0.85);
  font-weight: 700;
}

/* ── Mobile: two rows ── */
@media (max-width: 600px) {
  .nav-inner {
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.75rem 1.5rem;
  }

  .lang-selector {
    margin-left: 0;
    border-left: none;
    padding-left: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 0.4rem;
  }
}
</style>
