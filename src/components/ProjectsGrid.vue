<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ProjectCard from './ProjectCard.vue'
import rawProjects from '../assets/projects/manifest.json'

const headerImages = import.meta.glob('../assets/projects/*/header.png', { eager: true, import: 'default' })

const projects = [...rawProjects].sort(() => Math.random() - 0.5)

const screenWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1200)

function onResize() {
  screenWidth.value = window.innerWidth
}

onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))

const layout = computed(() => {
  const w = screenWidth.value
  if (w < 480) return { pattern: [2, 3, 2, 3, 2], size: 90, gap: 8 }
  if (w < 768) return { pattern: [2, 3, 2, 3, 2], size: 110, gap: 10 }
  return { pattern: [3, 4, 5], size: 170, gap: 16 }
})

const items = computed(() => {
  const { pattern, size, gap } = layout.value
  const maxCols = Math.max(...pattern)
  const cellW = size + gap
  const cellH = size + gap
  const totalW = maxCols * cellW
  const totalH = pattern.length * cellH

  const result = []
  let idx = 0

  
  for (let r = 0; r < pattern.length; r++) {
    const count = pattern[r]
    const rowW = count * cellW
    const offsetX = (totalW - rowW) / 2

    for (let c = 0; c < count; c++) {
      if (idx >= projects.length) break
      const proj = projects[idx]
      const key = `../assets/projects/${proj.titol}/header.png`
      result.push({
        ...proj,
        headerUrl: headerImages[key] || '',
        x: offsetX + c * cellW + cellW / 2 - totalW / 2,
        y: r * cellH + cellH / 2 - totalH / 2,
      })
      idx++
    }
  }

  return result
})
</script>

<template>
  <section id="projects" class="projects-section">
    <h2 class="section-title">Projects</h2>
    <div class="honeycomb" :style="{ '--cell-size': layout.size + 'px' }">
      <div
        v-for="item in items"
        :key="item.id"
        class="cell-wrapper"
        :style="{ transform: `translate(${item.x}px, ${item.y}px)` }"
      >
        <ProjectCard :titol="item.titol" :tipografia="item.tipografia" :rol="item.rol" :color="item.color" :headerUrl="item.headerUrl" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.projects-section {
  min-height: 100vh;
  background: #0f0c29;
  padding: 6rem 1rem 4rem;
  overflow: hidden;
}

.section-title {
  text-align: center;
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 3rem;
}

.honeycomb {
  position: relative;
  width: 100%;
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cell-wrapper {
  position: absolute;
  transition: transform 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
</style>
