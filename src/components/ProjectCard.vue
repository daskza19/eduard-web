<script setup>
defineProps({
  titol: String,
  tipografia: String,
  rol: String,
  color: String,
})
</script>

<template>
  <div class="cell" :style="{ '--accent': color }">
    <div class="cell-glow"></div>
    <span class="cell-title" :style="{ fontFamily: tipografia }">{{ titol }}</span>
    <span class="cell-rol">{{ rol }}</span>
  </div>
</template>

<style scoped>
.cell {
  width: var(--cell-size, 130px);
  height: var(--cell-size, 130px);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.07);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  overflow: hidden;
  position: relative;
  transition: box-shadow 0.4s ease,
              background 0.4s ease,
              border-color 0.4s ease;
}

.cell:hover {
  z-index: 10;
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow:
    0 0 40px color-mix(in srgb, var(--accent) 25%, transparent),
    0 15px 50px rgba(0, 0, 0, 0.4);
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
}

.cell-rol {
  display: inline-block;
  font-size: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
  border-radius: 99px;
  padding: 0.15rem 0.5rem;
  position: relative;
  white-space: nowrap;
}
</style>
