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
      <h1 class="hero-title">Eduard</h1>
      <p class="hero-phrase">Text provisional
      </p>
      <div class="scroll-hint">
        <span class="scroll-arrow">↓</span>
      </div>
    </div>
  </section>
</template>

<script setup>
// No logic needed — autoplay is handled by the browser
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

.hero-title {
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
  margin: 0;
}

.hero-phrase {
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 300;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

/* ── Scroll hint ── */
.scroll-hint {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.scroll-arrow {
  font-size: 3rem;
  color: rgb(145, 166, 124);
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0);   opacity: 0.8; }
  50%       { transform: translateY(8px); opacity: 1;   }
}
</style>