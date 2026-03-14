<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const visible = ref(false)
const activeSection = ref('projects')

const sections = ['projects', 'info', 'chronology']

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
      <a class="nav-link" :class="{ active: activeSection === 'projects' }" @click="scrollTo('projects')">PROJECTES</a>
      <a class="nav-link" :class="{ active: activeSection === 'info' }" @click="scrollTo('info')">SOBRE MÍ</a>
      <a class="nav-link" :class="{ active: activeSection === 'chronology' }" @click="scrollTo('chronology')">CRONOLOGÍA</a>
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
  background: rgba(73, 83, 62, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(72, 83, 61, 0.8);
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
}

.nav-link:hover {
  color: rgba(255, 255, 255, 0.6);
}

.nav-link.active {
  color: rgba(255, 255, 255, 0.85);
  font-weight: 700;
}
</style>
