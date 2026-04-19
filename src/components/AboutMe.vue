<script setup>
import { vTextId } from '../directives/textId.js'
</script>

<template>
  <section id="info" class="about">
    <!-- Decorative vertical line -->
    <div class="deco-line top-line"></div>

    <div class="about-layout">
      <!-- Left: contact + photo -->
      <div class="about-left">
        <div class="photo-area">
          <div class="photo-circle-bg"></div>
          <img
            src="../assets/images/hero.jpg"
            alt="Edu Arbona"
            class="about-photo"
          />
        </div>
      </div>

      <!-- Right: greeting + bio -->
      <div class="about-right">
        <h2 class="greeting">¡Hola!</h2>

        <div class="bio-card">
          <p>
            Soy <span class="highlight">Edu Arbona</span>, tengo 30 años y aquí os dejo mi reel-web.
          </p>
          <p>
            Esto pretende ser un <span class="underline-accent">recopilatorio de proyectos</span> que he hecho a lo largo de los tiempos.
          </p>
          <p>
            En 2018 finalicé mis estudios en la ESCAC, especializándome en
            <span class="highlight">Dirección de Arte</span> y actualmente estoy trabajando como:
            <span class="highlight">Regidor</span>, <span class="highlight">Props buyer</span> y/o <span class="highlight">Director de Arte</span>.
          </p>
        </div>

        <p class="tagline">
          Amante de la naturaleza 🌿, los colores 🎨 y las texturas 🏕.
        </p>
      </div>
    </div>

    <!-- Decorative leaves (CSS only) -->
    <div class="deco-leaves"></div>
  </section>
</template>

<style scoped>
.about {
  position: relative;
  min-height: 90vh;
  padding: 5rem 2rem 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
}

/* Decorative vertical line */
.deco-line {
  width: 2px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  margin-bottom: 2rem;
}

/* Main two-column layout */
.about-layout {
  display: flex;
  gap: 4rem;
  max-width: 960px;
  width: 100%;
  align-items: center;
}

/* ---- LEFT COLUMN ---- */
.about-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2rem;
  flex-shrink: 0;
}

.contact-block {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.85rem;
  line-height: 1.8;
}

.contact-heading {
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.4rem;
}

.contact-block a {
  color: #fff;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* Photo with decorative bg circle */
.photo-area {
  position: relative;
  width: 220px;
  height: 220px;
}

.photo-circle-bg {
  position: absolute;
  top: -15px;
  left: -15px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

.about-photo {
  position: relative;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.15);
  z-index: 1;
}

/* ---- RIGHT COLUMN ---- */
.about-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.greeting {
  font-size: clamp(2.5rem, 6vw, 3.5rem);
  font-weight: 800;
  color: #fff;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.bio-card {
  background: rgba(255, 255, 255, 0.07);
  border-left: 3px solid rgba(255, 255, 255, 0.25);
  border-radius: 0 1rem 1rem 0;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.05rem;
  line-height: 1.75;
}

.highlight {
  background: rgba(255, 255, 255, 0.12);
  padding: 0.1em 0.45em;
  border-radius: 0.3em;
  font-weight: 600;
  color: #fff;
}

.underline-accent {
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
  color: #fff;
}

.tagline {
  color: rgba(255, 255, 255, 0.55);
  font-size: 1rem;
  text-align: center;
  margin-top: 0.5rem;
}

/* ---- MOBILE ---- */
@media (max-width: 700px) {
  .about {
    padding: 3rem 1.25rem 3rem;
  }

  .deco-line {
    height: 50px;
    margin-bottom: 1.5rem;
  }

  .about-layout {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
    text-align: center;
  }

  .about-left {
    align-items: center;
    order: 1;
  }

  .about-right {
    order: 2;
    align-items: center;
  }

  .contact-block {
    text-align: center;
    order: 2;
  }

  .photo-area {
    width: 170px;
    height: 170px;
    order: 1;
  }

  .photo-circle-bg {
    width: 150px;
    height: 150px;
  }

  .about-photo {
    width: 170px;
    height: 170px;
  }

  .greeting {
    font-size: 2.2rem;
  }

  .bio-card {
    padding: 1.25rem 1.25rem;
    font-size: 0.95rem;
    border-left: none;
    border-top: 3px solid rgba(255, 255, 255, 0.25);
    border-radius: 0 0 1rem 1rem;
    text-align: left;
  }
}
</style>
