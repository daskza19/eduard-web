<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n.js'

const { t } = useI18n()

const props = defineProps({
  titol: String,
  tipografia: String,
  rol: String,
  color: String,
  headerUrl: String,
  projectType: String,
})

const translatedRol = computed(() => t(props.rol))

const catColorMap = {
  VIDEOCLIP: 'var(--cat-videoclip-bg)',
  MODA: 'var(--cat-moda-bg)',
  FESTIVAL: 'var(--cat-festival-bg)',
  PODCAST: 'var(--cat-podcast-bg)',
  ANUNCI: 'var(--cat-anunci-bg)',
  DIRECTOR_ART: 'var(--cat-director-art-bg)',
}

const catColor = computed(() => catColorMap[props.projectType] || 'transparent')
</script>

<template>
  <div class="cell" :class="projectType" :style="{ '--accent': color, '--cat-color': catColor }">
    <div class="cell-bg" :style="{ backgroundImage: headerUrl ? `url(${JSON.stringify(headerUrl)})` : 'none' }"></div>
    <div class="cell-glow"></div>
    <div class="cell-info">
      <span class="cell-title" :style="{ fontFamily: tipografia }">{{ titol }}</span>
      <span class="cell-rol" :class="rol">{{ translatedRol }}</span>
      <span class="cell-type" :class="projectType">{{ projectType }}</span>
    </div>
  </div>
</template>

<style scoped>
.cell {
  width: var(--cell-size, 170px);
  height: var(--cell-size, 170px);
  background-color: rgba(255, 255, 255, 0.04);
  border: 3px solid;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  overflow: hidden;
  position: relative;
  border-radius: 0.5rem;
  transition: transform 0.35s ease,
              box-shadow 0.35s ease,
              border-color 0.35s ease,
              filter 0.35s ease;
}

.cell:hover {
  z-index: 10;
  transform: scale(1.08);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow:
    0 0 40px color-mix(in srgb, var(--accent) 25%, transparent),
    0 15px 50px rgba(0, 0, 0, 0.4);
}

.cell-bg {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  transition: filter 0.35s ease,
              transform 0.35s ease;
  pointer-events: none;
}

.cell-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--cat-color, transparent);
  mix-blend-mode: color;
  opacity: 0;
  transition: opacity 0.35s ease;
  pointer-events: none;
}

.cell:hover .cell-bg {
  filter: blur(3px) brightness(0.8) saturate(1);
  transform: scale(1.05);
}

.cell:hover .cell-bg::after {
  opacity: 0.5;
}

.cell-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-items: end;
  gap: 0.4rem;
  position: relative;
  z-index: 1;
}

@media (min-width: 768px) {
  .cell-info {
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  .cell:hover .cell-info {
    opacity: 1;
  }
}

.cell-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--accent);
  opacity: 0.25;
  filter: blur(18px);
  transform: translate(-50%, -50%);
  transition: opacity 0.4s, transform 0.4s;
  pointer-events: none;
}

.cell:hover .cell-glow {
  opacity: 0.5;
  transform: translate(-50%, -50%) scale(2.5);
}

.cell-title {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  position: relative;
  text-align: center;
  line-height: 1.2;
  padding: 0 0.4rem;
  text-shadow:
    -1px -1px 0 #353535,
     1px -1px 0 #353535,
    -1px  1px 0 #353535,
     1px  1px 0 #353535;
}

.cell-rol {
  display: inline-block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  color: var(--accent);
  background: rgb(100, 100, 100);
  border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
  border-radius: 99px;
  padding: 0.15rem 0.5rem;
  position: relative;
  white-space: nowrap;
}

.cell-type {
  display: inline-block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  color: var(--accent);
  background-color: rgb(145, 145, 145);
  border: 1px solid rgb(99, 99, 99);
  border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
  border-radius: 99px;
  padding: 0.15rem 0.5rem;
  position: relative;
  white-space: nowrap;
  border: 1px solid;
}

.VIDEOCLIP {
  background-color: var(--cat-videoclip-bg);
  border-color: var(--cat-videoclip-border);
}

.MODA {
  background-color: var(--cat-moda-bg);
  border-color: var(--cat-moda-border);
}

.FESTIVAL {
  background-color: var(--cat-festival-bg);
  border-color: var(--cat-festival-border);
}

.PODCAST {
  background-color: var(--cat-podcast-bg);
  border-color: var(--cat-podcast-border);
}

.ANUNCI {
  background-color: var(--cat-anunci-bg);
  border-color: var(--cat-anunci-border);
}

.DIRECTOR_ART {
  background-color: var(--cat-director-art-bg);
  border-color: var(--cat-director-art-border);
}
</style>
