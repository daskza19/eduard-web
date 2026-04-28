<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { vTextId } from '../directives/textId.js'
import chronologyData from '../assets/chronology/manifest.json'

// Reverse chronological order: newest first
const data = [...chronologyData].reverse().map(y => ({
  ...y,
  events: [...y.events].reverse()
}))
const years = data.map(y => y.year)

// Flatten all events preserving year reference
const allEvents = []
data.forEach((yearGroup, yearIdx) => {
  yearGroup.events.forEach((event) => {
    allEvents.push({
      ...event,
      year: yearGroup.year,
      yearIndex: yearIdx,
      id: `evt-${allEvents.length}`
    })
  })
})

const TOTAL = allEvents.length
const SCROLL_PER_EVENT = 120

const sectionRef = ref(null)
const progress = ref(0)
const vh = ref(800)
const vw = ref(1024)

const totalHeight = computed(() => TOTAL * SCROLL_PER_EVENT + vh.value)
const activeIdx = computed(() => Math.min(Math.round(progress.value), TOTAL - 1))
const activeYear = computed(() => allEvents[activeIdx.value]?.yearIndex ?? 0)
const activeEvtHeight = ref(70)
const evtTrackRef = ref(null)

// Only render events near the active one for performance
const visibleEvents = computed(() => {
  const c = activeIdx.value
  const items = []
  for (let i = Math.max(0, c - 6); i <= Math.min(TOTAL - 1, c + 6); i++) {
    items.push({ ...allEvents[i], _i: i })
  }
  return items
})

function eventStyle(i) {
  const off = i - progress.value
  const abs = Math.abs(off)
  if (abs > 6) return { visibility: 'hidden', position: 'absolute', top: '50%', width: '100%' }
  const sp = vw.value < 768 ? 100 : 85
  const y = off * sp
  return {
    transform: `translateY(calc(-50% + ${y}px)) scale(${Math.max(0.82, 1 - abs * 0.04)})`,
    opacity: Math.max(0, 1 - abs * 0.26),
    zIndex: 6 - Math.min(6, Math.round(abs))
  }
}

function yearStyle(i) {
  const off = i - activeYear.value
  const abs = Math.abs(off)
  const sp = vw.value < 768 ? 42 : 55
  const y = off * sp
  return {
    transform: `translateY(calc(-50% + ${y}px)) scale(${abs === 0 ? 1 : Math.max(0.6, 1 - abs * 0.12)})`,
    opacity: Math.max(0.08, 1 - abs * 0.3),
    fontWeight: abs === 0 ? 800 : 400,
    zIndex: 6 - Math.min(6, Math.round(abs))
  }
}

function scrollToYear(idx) {
  if (!sectionRef.value) return
  const ei = allEvents.findIndex(e => e.yearIndex === idx)
  if (ei < 0) return
  const top = sectionRef.value.offsetTop
  const max = sectionRef.value.offsetHeight - vh.value
  window.scrollTo({ top: top + (ei / (TOTAL - 1)) * max, behavior: 'smooth' })
}

let rafId = null
let snapTimer = null
let isSnapping = false

function getScrollMax() {
  if (!sectionRef.value) return 1
  return sectionRef.value.offsetHeight - vh.value
}

function onScroll() {
  if (rafId) return
  rafId = requestAnimationFrame(() => {
    rafId = null
    if (!sectionRef.value) return
    const t = -sectionRef.value.getBoundingClientRect().top
    const max = getScrollMax()
    if (max <= 0) return
    progress.value = Math.max(0, Math.min(TOTAL - 1, (t / max) * (TOTAL - 1)))

    // Measure active event height
    if (evtTrackRef.value) {
      const activeEl = evtTrackRef.value.querySelector('.evt.active')
      if (activeEl) {
        const h = activeEl.offsetHeight
        if (h > 0) activeEvtHeight.value = h + 8
      }
    }

    // Schedule snap after user stops scrolling
    if (!isSnapping) {
      clearTimeout(snapTimer)
      snapTimer = setTimeout(snapToNearest, 120)
    }
  })
}

function snapToNearest() {
  if (!sectionRef.value) return
  const nearest = Math.round(progress.value)
  if (Math.abs(progress.value - nearest) < 0.02) return
  const max = getScrollMax()
  const targetScroll = sectionRef.value.offsetTop + (nearest / (TOTAL - 1)) * max
  isSnapping = true
  window.scrollTo({ top: targetScroll, behavior: 'smooth' })
  setTimeout(() => { isSnapping = false }, 400)
}

function onResize() {
  vh.value = window.innerHeight
  vw.value = window.innerWidth
}

function parseEnf(text) {
  if (!text) return ''
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/&lt;enf&gt;(.*?)&lt;\/enf&gt;/g, '<strong>$1</strong>')
}

function fmtRole(r) {
  return r ? r.replace(/_/g, ' ') : ''
}

onMounted(() => {
  vh.value = window.innerHeight
  vw.value = window.innerWidth
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })
  nextTick(onScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onResize)
  if (rafId) cancelAnimationFrame(rafId)
  clearTimeout(snapTimer)
})
</script>

<template>
  <section id="chronology" ref="sectionRef" class="chrono" :style="{ height: totalHeight + 'px' }">
    <div class="sticky">
      <div class="columns">
        <!-- Year wheel -->
        <div class="wheel year-col">
          <div class="indicator"></div>
          <div class="track">
            <div
              v-for="(yr, i) in years"
              :key="yr"
              class="yr"
              :class="{ active: i === activeYear }"
              :style="yearStyle(i)"
              @click="scrollToYear(i)"
            >{{ yr }}</div>
          </div>
          <div class="fade fade-t"></div>
          <div class="fade fade-b"></div>
        </div>

        <!-- Event wheel -->
        <div class="wheel evt-col">
          <div class="indicator" :style="{ height: activeEvtHeight + 'px' }"></div>
          <div ref="evtTrackRef" class="track">
            <div
              v-for="ev in visibleEvents"
              :key="ev.id"
              class="evt"
              :class="{ active: ev._i === activeIdx, 'other-year': ev.yearIndex !== activeYear }"
              :style="eventStyle(ev._i)"
            >
              <div class="evt-head">
                <span class="evt-date">{{ ev.data }}</span>
                <span v-if="ev.rol1" class="evt-role">{{ fmtRole(ev.rol1) }}</span>
                <span v-if="ev.rol2" class="evt-role">{{ fmtRole(ev.rol2) }}</span>
              </div>
              <div class="evt-text" v-html="parseEnf(ev.text)"></div>
              <div v-if="ev.sub_text" class="evt-sub" v-html="parseEnf(ev.sub_text)"></div>
            </div>
          </div>
          <div class="fade fade-t"></div>
          <div class="fade fade-b"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.chrono {
  position: relative;
}

.sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  overflow: hidden;
}

.title {
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
  text-align: center;
  flex-shrink: 0;
  padding-top: 10vh;
}

.columns {
  display: flex;
  gap: 2rem;
  width: 100%;
  max-width: 1000px;
  flex: 1;
  min-height: 0;
}

/* ── Wheel shared ── */
.wheel {
  position: relative;
  overflow: hidden;
}

.year-col {
  width: 300px;
  min-width: 20vw;
  flex-shrink: 0;
}

.evt-col {
  flex: 1;
  min-width: 0;
}

.track {
  position: relative;
  width: 100%;
  height: 100%;
}

.indicator {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 72px;
  transform: translateY(-50%);
  transition: height 0.25s ease;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.03);
  border-radius: 4px;
  pointer-events: none;
  z-index: 20;
}

.fade {
  position: absolute;
  left: 0;
  right: 0;
  height: 38%;
  pointer-events: none;
  z-index: 15;
}

.fade-t {
  top: 0;
  background: linear-gradient(to bottom, rgb(24, 24, 24) 15%, transparent);
}

.fade-b {
  bottom: 0;
  background: linear-gradient(to top, rgb(24, 24, 24) 15%, transparent);
}

/* ── Year items ── */
.yr {
  position: absolute;
  top: 50%;
  width: 100%;
  text-align: center;
  font-size: 1.8rem;
  color: rgba(255, 255, 255, 0.45);
  cursor: pointer;
  user-select: none;
  line-height: 1;
  transition:
    color 0.3s,
    font-weight 0.15s,
    transform 0.35s cubic-bezier(0.25, 0.1, 0.25, 1),
    opacity 0.35s;
  will-change: transform, opacity;
}

.yr.active {
  color: #fff;
  font-size: 2.2rem;
}

/* ── Event items ── */
.evt {
  position: absolute;
  top: 50%;
  width: 100%;
  padding: 0.4rem 0.8rem;
  will-change: transform, opacity;
}

.evt-head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.15rem;
}

.evt-date {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.03em;
  font-weight: 500;
}

.evt-role {
  font-size: 0.8rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.75);
  background: var(--main-primary-light-chars);
  padding: 0.12rem 0.45rem;
  border-radius: 3px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.evt-text {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.55);
  line-height: 1.4;
  transition: color 0.15s;
}

.evt.active .evt-text {
  color: rgba(255, 255, 255, 0.9);
}

.evt-text :deep(strong) {
  color: #fff;
  font-weight: 700;
}

.evt-sub {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.22);
  margin-top: 0.1rem;
  line-height: 1.3;
}

.evt.active .evt-sub {
  color: rgba(255, 255, 255, 0.4);
}

/* Events from a different year */
.evt.other-year .evt-date {
  color: rgba(255, 255, 255, 0.15);
}

.evt.other-year .evt-role {
  background: rgba(82, 95, 70, 0.25);
  color: rgba(255, 255, 255, 0.35);
}

.evt.other-year .evt-text {
  color: rgba(255, 255, 255, 0.22);
}

.evt.other-year .evt-text :deep(strong) {
  color: rgba(255, 255, 255, 0.35);
}

.evt.other-year .evt-sub {
  color: rgba(255, 255, 255, 0.1);
}

/* ── Mobile: stack vertically ── */
@media (max-width: 768px) {
  .columns {
    flex-direction: column;
    gap: 0;
  }

  .year-col {
    margin-top: 2vh;
    width: 80%;
    height: 20vh;
    flex-shrink: 0;
    align-self: center;
  }

  .evt-col {
    z-index: -1;
    flex: 1;
    margin-top: -10vh;
    width: 80%;
    align-self: center;
  }

  .yr {
    font-size: 2rem;
  }

  .yr.active {
    font-size: 2.2rem;
  }

  .indicator {
    height: 55px;
  }

  .sticky {
    padding: 6rem 0 2rem 0;
  }

  .title {
    margin-bottom: 0.5rem;
  }
}
</style>
