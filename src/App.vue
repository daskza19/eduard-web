<script setup>
import NavBar from './components/NavBar.vue'
import ProjectsGrid from './components/ProjectsGrid.vue'
import Hero from './components/Hero.vue'
import { vTextId } from './directives/textId.js'
</script>

<template>
  <NavBar />
  <Hero />

  <ProjectsGrid />

  <section id="info" class="content-section">
    <h2 class="section-title" v-text-id="'info_title'"></h2>
    <p class="section-text">
      Text provisional
    </p>
  </section>

  <section id="chronology" class="content-section">
    <h2 class="section-title" v-text-id="'chronology_title'"></h2>
    <div class="timeline">
      <div class="timeline-item" v-for="item in [
        { year: '2024', text: 'Test' },
        { year: '2025', text: 'Test' },
        { year: '2026', text: 'Test' },
      ]" :key="item.year">
        <span class="timeline-year">{{ item.year }}</span>
        <p class="timeline-text">{{ item.text }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.scroll-hint {
  margin-top: 3rem;
  animation: bounce 2s infinite;
}

.scroll-arrow {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.3);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(10px); }
}

/* Shared section styles */
.content-section {
  min-height: 80vh;
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 2rem;
  text-align: center;
}

.section-text {
  max-width: 600px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  line-height: 1.8;
  text-align: center;
}

/* Timeline */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  max-width: 600px;
  width: 100%;
  border-left: 2px solid rgba(82, 95, 70, 0.3);
  padding-left: 2rem;
}

.timeline-item {
  position: relative;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -2.55rem;
  top: 0.35rem;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgb(82, 95, 70);
}

.timeline-year {
  font-size: 0.85rem;
  font-weight: 700;
  color: rgb(82, 95, 70);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.timeline-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin-top: 0.3rem;
  line-height: 1.6;
}
</style>
