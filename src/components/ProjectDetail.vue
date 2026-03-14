<script setup>
import { computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  project: Object,
})

const emit = defineEmits(['close'])

// ── Main images (eager glob) ──
const mainImages = import.meta.glob(
  '../assets/projects/*/main.{png,jpg,jpeg,webp,gif,svg,avif}',
  { eager: true, import: 'default' }
)

// ── Asset images (eager glob) ──
const assetImages = import.meta.glob(
  '../assets/projects/*/assets/*.{png,jpg,jpeg,webp,gif,svg,avif}',
  { eager: true, import: 'default' }
)

const mainUrl = computed(() => {
  const prefix = `../assets/projects/${props.project.titol}/main.`
  const key = Object.keys(mainImages).find(k => k.startsWith(prefix))
  return key ? mainImages[key] : ''
})

const galleryUrls = computed(() => {
  const folder = `../assets/projects/${props.project.titol}/assets/`
  return (props.project.assets || [])
    .map(filename => {
      const full = folder + filename
      return assetImages[full] || ''
    })
    .filter(Boolean)
})

const embedUrl = computed(() => {
  const v = props.project.video
  if (!v) return ''

  // YouTube
  const ytMatch = v.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)/)
  if (ytMatch) return `https://www.youtube-nocookie.com/embed/${encodeURIComponent(ytMatch[1])}`

  // Vimeo
  const vmMatch = v.match(/vimeo\.com\/(\d+)/)
  if (vmMatch) return `https://player.vimeo.com/video/${encodeURIComponent(vmMatch[1])}`

  return ''
})

function onKeydown(e) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div class="detail-overlay" @click.self="emit('close')">
    <div class="detail-modal">
      <button class="close-btn" @click="emit('close')">&times;</button>

      <!-- 1. Hero: main image + info -->
      <section class="detail-hero">
        <img :src="mainUrl" :alt="project.titol" class="hero-img" />
        <div class="hero-info">
          <h1 class="hero-title">{{ project.titol }}</h1>
          <p v-if="project.subtitol" class="hero-subtitle">{{ project.subtitol }}</p>
          <p v-if="project.productora" class="hero-productora">{{ project.productora }}</p>
        </div>
      </section>

      <!-- 2. Video embed -->
      <section v-if="embedUrl" class="detail-video">
        <div class="video-container">
          <iframe
            :src="embedUrl"
            frameborder="0"
            allow="autoplay; fullscreen; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      </section>

      <!-- 3. Gallery grid -->
      <section v-if="galleryUrls.length" class="detail-gallery">
        <div class="gallery-grid">
          <img
            v-for="(url, i) in galleryUrls"
            :key="i"
            :src="url"
            :alt="`${project.titol} - ${i + 1}`"
            class="gallery-img"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ── Overlay ── */
.detail-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* ── Modal ── */
.detail-modal {
  position: relative;
  background: #1a1e16;
  width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 1rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(145, 166, 124, 0.4) transparent;
  padding: 0;
  margin: 0;
}

.close-btn {
  position: fixed;
  top: calc(5vh + 1rem);
  right: calc(5vw + 1rem);
  z-index: 210;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: #fff;
  font-size: 2rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.8);
}

/* ── 1. Hero section ── */
.detail-hero {
  position: relative;
  height: 90vh;
  width: 100%;
  overflow: hidden;
}

.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-info {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 3rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  width: 30vw;
  margin-top: 2vw;
  margin-left: 2vw;
  border-radius: 2rem;
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  color: #fff;
  margin: 0;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: clamp(0.9rem, 1.5vw, 1.1rem);
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  line-height: 1.5;
  max-width: 600px;
}

.hero-productora {
  font-size: 0.85rem;
  color: rgba(145, 166, 124, 0.8);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

/* ── 2. Video section ── */
.detail-video {
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 0.5rem;
}

/* ── 3. Gallery section ── */
.detail-gallery {
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  width: 100%;
}

.gallery-img {
  width: 100%;
  border-radius: 0.5rem;
  object-fit: cover;
  aspect-ratio: 1;
  transition: transform 0.3s ease;
}

.gallery-img:hover {
  transform: scale(1.03);
}

/* ── Mobile: fullscreen ── */
@media (max-width: 767px) {
  .detail-modal {
    width: 100vw;
    max-width: none;
    max-height: none;
    height: 100vh;
    border-radius: 0;
  }

  .close-btn {
    top: 1rem;
    right: 1rem;
  }

  .hero-info {
    padding: 2rem 1.5rem;
  }

  .detail-video {
    padding: 1rem;
  }

  .detail-gallery {
    padding: 1rem;
  }

  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 0.5rem;
  }

  .gallery-img:hover {
    transform: none;
  }
}
</style>
