<template>
  <section class="hero">
    <video
      class="hero-video"
      autoplay
      muted
      loop
      playsinline
      poster="../assets/images/hero.jpg"
    >
      <source src="../assets/images/hero.webm" type="video/webm" />
      <source src="../assets/images/hero.mp4" type="video/mp4" />
    </video>

    <div class="hero-overlay" />

    <div class="hero-content">
      <canvas ref="lottieCanvas" class="hero-lottie"></canvas>
      <p class="hero-phrase" v-text-id="'hero_title'"></p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { DotLottie } from '@lottiefiles/dotlottie-web'
import { vTextId } from '../directives/textId.js'
import lottieUrl from '../assets/images/EDUARD LOGO.lottie?url'

const lottieCanvas = ref(null)
let dotLottie = null

function resizeCanvas() {
  const canvas = lottieCanvas.value
  if (!canvas) return
  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
}

onMounted(() => {
  resizeCanvas()
  dotLottie = new DotLottie({
    canvas: lottieCanvas.value,
    src: lottieUrl,
    autoplay: true,
    loop: true,
  })
  window.addEventListener('resize', resizeCanvas)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeCanvas)
  if (dotLottie) dotLottie.destroy()
})
</script>

<style scoped>
.hero {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(145, 166, 124, 0.01) 0%,
    rgba(145, 166, 124, 0.01) 50%,
    rgba(145, 166, 124, 0.4) 85%,
    rgba(145, 166, 124, 1.0) 100%
  );
  z-index: 1;
}

/* ── Vídeo ── */
.hero-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  z-index: 0;
  pointer-events: none;
}

/* ── Contenido centrado ── */
.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.hero-lottie {
  width: clamp(280px, 50vw, 600px);
  height: auto;
}

.hero-phrase {
  font-size: clamp(1.25rem, 3vw, 1.25rem);
  font-weight: 500;
  color: rgb(0, 0, 0);
  padding: 0.1rem 0.2rem;
  background: rgb(255, 255, 255);
}
</style>