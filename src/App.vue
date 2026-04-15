<script setup>
import NavBar from './components/NavBar.vue'
import ProjectsGrid from './components/ProjectsGrid.vue'
import Hero from './components/Hero.vue'
import Chronology from './components/Chronology.vue'
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

  <Chronology />
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


</style>
