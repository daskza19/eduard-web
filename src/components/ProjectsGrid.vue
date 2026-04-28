<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ProjectCard from './ProjectCard.vue'
import ProjectDetail from './ProjectDetail.vue'
import rawProjects from '../assets/projects/manifest.json'

const headerImages = import.meta.glob('../assets/projects/*/header.{png,jpg,jpeg,webp,gif,svg,avif}', { eager: true, import: 'default' })

function findHeader(titol) {
  const prefix = `../assets/projects/${titol}/header.`
  const key = Object.keys(headerImages).find(k => k.startsWith(prefix))
  return key ? headerImages[key] : ''
}


// Mostrar los proyectos en el orden inverso al del manifest.json
const projects = [...rawProjects].reverse();

// Chips de categorías
const categories = computed(() => {
  // Extraer categorías únicas en el orden de aparición (inverso)
  const set = new Set();
  projects.forEach(p => set.add(p.categoria));
  return Array.from(set);
});

const selectedCategory = ref(null); // null = todas

const filteredProjects = computed(() => {
  if (!selectedCategory.value) return projects;
  return projects.filter(p => p.categoria === selectedCategory.value);
});

const screenWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1200)

function onResize() {
  screenWidth.value = window.innerWidth
}

onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))

const layout = computed(() => {
  const w = screenWidth.value
  // Definir patrones y tamaños base
  let pattern, baseSize, gap
  if (w < 480) {
    pattern = [3, 4, 3, 4, 3, 4, 3, 4];
    baseSize = 90;
    gap = 8;
  } else if (w < 768) {
    pattern = [3, 4, 3, 4, 3, 4, 3, 4];
    baseSize = 110;
    gap = 10;
  } else {
    pattern = [5, 6, 7, 6, 5];
    baseSize = 170;
    gap = 16;
  }
  // Calcular el ancho máximo de la grid
  const maxRow = Math.max(...pattern);
  const maxGridWidth = w - 32; // padding de la sección
  const totalCardWidth = maxRow * baseSize + (maxRow - 1) * gap;
  let size = baseSize;
  if (totalCardWidth > maxGridWidth) {
    size = Math.floor((maxGridWidth - (maxRow - 1) * gap) / maxRow);
  }
  return { pattern, size, gap };
})

const hoveredIdx = ref(-1)
const selectedProject = ref(null)

function openProject(item) {
  selectedProject.value = item
}

// --- Tunables ---
const EDGE_SHRINK = 0       // how much smaller edge cards are (0 = same, 1 = invisible)
const HOVER_SCALE = 1.1       // scale of the hovered card
const NEIGHBOR_BOOST = 0.2    // max extra scale for nearby cards on hover
const NEIGHBOR_MAX = 1.05      // cap scale for neighbor cards
const NEIGHBOR_RADIUS = 1    // radius in cell-units for neighbor influence

const items = computed(() => {
  const { pattern, size, gap } = layout.value
  const totalRows = pattern.length
  const midRow = (totalRows - 1) / 2
  const projs = filteredProjects.value;

  // First pass: assign to rows and compute scale per card
  const rows = []
  let idx = 0
  for (let r = 0; r < totalRows; r++) {
    const count = pattern[r]
    const midCol = (count - 1) / 2
    const row = []
    for (let c = 0; c < count; c++) {
      if (idx >= projs.length) break
      const proj = projs[idx++]
      const ny = midRow > 0 ? (r - midRow) / midRow : 0
      const nx = midCol > 0 ? (c - midCol) / midCol : 0
      const dist = Math.sqrt(nx * nx + ny * ny)
      const scale = 1 - Math.min(dist / Math.SQRT2, 1) * EDGE_SHRINK
      row.push({ proj, scale })
    }
    rows.push(row)
  }

  // Second pass: position with consistent gaps between rendered edges
  const rowHeights = rows.map(row =>
    row.length > 0 ? Math.max(...row.map(c => size * c.scale)) : 0
  )
  const totalH = rowHeights.reduce((s, h) => s + h, 0) + (totalRows - 1) * gap

  const result = []
  let yAccum = -totalH / 2

  for (let r = 0; r < rows.length; r++) {
    const row = rows[r]
    const rowH = rowHeights[r]
    const cy = yAccum + rowH / 2

    const totalRowW = row.reduce((s, c) => s + size * c.scale, 0) + (row.length - 1) * gap
    let xAccum = -totalRowW / 2

    for (let c = 0; c < row.length; c++) {
      const card = row[c]
      const cardW = size * card.scale
      const cx = xAccum + cardW / 2

      result.push({
        ...card.proj,
        headerUrl: findHeader(card.proj.titol),
        x: cx,
        y: cy,
        scale: card.scale,
      })

      xAccum += cardW + gap
    }

    yAccum += rowH + gap
  }

  return result
})

function cellStyle(item, idx) {
  let scale = item.scale

  if (hoveredIdx.value >= 0) {
    const hovered = items.value[hoveredIdx.value]
    const dx = item.x - hovered.x
    const dy = item.y - hovered.y
    const d = Math.sqrt(dx * dx + dy * dy)
    const { size, gap } = layout.value
    const radius = (size + gap) * NEIGHBOR_RADIUS

    if (idx === hoveredIdx.value) {
      scale = HOVER_SCALE
    } else if (d < radius) {
      const proximity = 1 - d / radius
      scale = Math.min(scale + proximity * NEIGHBOR_BOOST, NEIGHBOR_MAX)
    }
  }

  return {
    transform: `translate(${item.x}px, ${item.y}px) scale(${scale})`,
    zIndex: idx === hoveredIdx.value ? 10 : 1,
  }
}
</script>

<template>
  <section id="projects" class="projects-section">
    <!-- Chips de categorías -->
    <div class="category-chips-row">
      <span
        class="category-chip"
        :class="{ selected: !selectedCategory }"
        @click="selectedCategory = null"
      >
        Todas
      </span>
      <span
        v-for="cat in categories"
        :key="cat"
        class="category-chip"
        :class="{ selected: selectedCategory === cat }"
        @click="selectedCategory = cat"
      >
        {{ cat }}
      </span>
    </div>
    <div class="honeycomb" :style="{ '--cell-size': layout.size + 'px' }">
      <div
        v-for="(item, idx) in items"
        :key="item.id + '-' + idx"
        class="cell-wrapper"
        :style="cellStyle(item, idx)"
        @mouseenter="hoveredIdx = idx"
        @mouseleave="hoveredIdx = -1"
        @click="openProject(item)"
      >
        <ProjectCard :titol="item.titol" :tipografia="item.tipografia" :rol="item.rol" :color="item.color" :headerUrl="item.headerUrl" :projectType="item.categoria" />
      </div>
    </div>

    <ProjectDetail
      v-if="selectedProject"
      :project="selectedProject"
      @close="selectedProject = null"
    />
  </section>
</template>

<style scoped>

.projects-section {
  min-height: 100vh;
  padding: 6rem 1rem 4rem;
  overflow: hidden;
}

.category-chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.category-chip {
  display: inline-block;
  padding: 0.18rem 0.9rem;
  border-radius: 99px;
  color: var(--main-primary-light);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border: 1px solid var(--main-primary-light-border);
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border 0.2s;
  user-select: none;
}
.category-chip.selected, .category-chip:hover {
  background: var(--main-primary-light);
  color: var(--main-primary);
  border: 1px solid var(--main-primary-light-border);
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
  width: 100vw;
  max-width: 100vw;
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
  margin-left: 50%;
  transform: translateX(-50%);
}

.cell-wrapper {
  position: absolute;
  transition: transform 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
</style>
