<script setup>
import NavBar from './components/NavBar.vue'
import ProjectsGrid from './components/ProjectsGrid.vue'
</script>

<template>
  <NavBar />

  <section class="hero">
    <div class="hero-content">
      <h1 class="hero-title">Eduard</h1>
      <p class="hero-phrase">Creando experiencias digitales que inspiran</p>
      <div class="scroll-hint">
        <span class="scroll-arrow">&#8595;</span>
      </div>
    </div>
  </section>

  <ProjectsGrid />

  <section id="info" class="content-section">
    <h2 class="section-title">Info</h2>
    <p class="section-text">
      Diseñador y desarrollador con pasión por crear experiencias
      digitales únicas que conectan personas con ideas.
    </p>
  </section>

  <section id="chronology" class="content-section">
    <h2 class="section-title">Chronology</h2>
    <div class="timeline">
      <div class="timeline-item" v-for="item in [
        { year: '2024', text: 'Inicio del viaje creativo' },
        { year: '2025', text: 'Primeros proyectos freelance' },
        { year: '2026', text: 'Expansión digital' },
      ]" :key="item.year">
        <span class="timeline-year">{{ item.year }}</span>
        <p class="timeline-text">{{ item.text }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  padding: 2rem;
}

.hero-content {
  text-align: center;
  max-width: 800px;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 700;
  margin: 0 0 1rem;
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-phrase {
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-weight: 300;
  letter-spacing: 0.02em;
  line-height: 1.6;
}

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
  background: #0f0c29;
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
  border-left: 2px solid rgba(102, 126, 234, 0.3);
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
  background: #667eea;
}

.timeline-year {
  font-size: 0.85rem;
  font-weight: 700;
  color: #667eea;
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
