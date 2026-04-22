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
      <h1 class="hero-phrase" v-text-id="'hero_title'"></h1>
      <p class="hero-subtitle" v-text-id="'hero_subtitle'"></p>
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
    rgba(24,24,24, 0.01) 0%,
    rgba(24,24,24, 0.01) 50%,
    rgba(24,24,24, 0.4) 80%,
    rgba(24,24,24, 1.0) 100%
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
  filter: saturate(150%);
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
  width:  clamp(350px, 50vw, 600px);
  height: auto;
}

.hero-phrase {
  font-family: 'Brams', sans-serif;
  font-size: 5rem;
  font-weight: 500;
  color: rgb(255, 255, 255);
  padding: 0.1rem 0.2rem;
  line-height: 4rem;
}

.hero-subtitle {
  font-family: 'GingerBrand', sans-serif;
  font-size: clamp(2rem, 2vw, 2.5rem);
  font-weight: normal;
  color: rgb(255, 255, 255);
  margin: 0;
}
</style>