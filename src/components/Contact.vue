<script setup>
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n.js'
import { vTextId } from '../directives/textId.js'
import { supabase } from '../lib/supabase.js'

const { t } = useI18n()

const form = ref({ name: '', email: '', message: '' })
const status = ref('') // '', 'sending', 'sent', 'error'

async function handleSubmit() {
  if (!supabase) {
    status.value = 'error'
    return
  }
  status.value = 'sending'
  try {
    const { data, error } = await supabase.functions.invoke('contact', {
      body: {
        name: form.value.name,
        email: form.value.email,
        message: form.value.message,
      },
    })
    if (error) {
      status.value = 'error'
    } else {
      status.value = 'sent'
      form.value = { name: '', email: '', message: '' }
    }
  } catch {
    status.value = 'error'
  }
}

const socials = [
  { name: 'Instagram', url: 'https://www.instagram.com/youngard/', icon: 'instagram' },
  { name: 'Vimeo', url: 'https://vimeo.com/youngard', icon: 'vimeo' },
  { name: 'YouTube', url: 'https://www.youtube.com/c/eduardsanchezarbona', icon: 'youtube' }
]
</script>

<template>
  <section id="contact" class="contact">
    <div class="contact-grid">
      <!-- Redes sociales -->
      <div class="contact-socials">
        <h3 class="contact-subtitle" v-text-id="'contact_socials'"></h3>
        <div class="socials-list">
          <a
            v-for="s in socials"
            :key="s.name"
            :href="s.url"
            target="_blank"
            rel="noopener noreferrer"
            class="social-link"
            :aria-label="s.name"
          >
            <!-- Instagram -->
            <svg v-if="s.icon === 'instagram'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
              <circle cx="12" cy="12" r="5"/>
              <circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none"/>
            </svg>
            <!-- Vimeo -->
            <svg v-else-if="s.icon === 'vimeo'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22 7.42c-.1 2.1-1.56 4.98-4.38 8.64C14.7 19.94 12.18 22 10.1 22c-1.28 0-2.38-1.18-3.26-3.56L5.16 12.3C4.54 9.92 3.86 8.74 3.12 8.74c-.16 0-.74.34-1.72 1.04L0 8.08c1.08-.96 2.14-1.92 3.2-2.86 1.44-1.24 2.52-1.9 3.24-1.96 1.7-.16 2.76 1 3.16 3.5.44 2.68.74 4.36.92 5.02.5 2.3 1.06 3.46 1.66 3.46.46 0 1.18-.74 2.12-2.22.94-1.48 1.46-2.6 1.52-3.38.14-1.28-.36-1.92-1.52-1.92-.54 0-1.1.12-1.68.38 1.12-3.66 3.24-5.44 6.4-5.32 2.34.06 3.44 1.58 3.32 4.56z"/>
            </svg>
            <!-- YouTube -->
            <svg v-else-if="s.icon === 'youtube'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.38.55A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.55 9.38.55 9.38.55s7.5 0 9.38-.55a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.54 15.57V8.43L15.82 12l-6.28 3.57z"/>
            </svg>

            <span>{{ s.name }}</span>
          </a>
        </div>
      </div>

      <!-- Formulario de contacto -->
      <form class="contact-form" @submit.prevent="handleSubmit">
        <h3 class="contact-subtitle" v-text-id="'contact_form_title'"></h3>

        <input
          v-model="form.name"
          type="text"
          :placeholder="t('contact_name')"
          required
          class="form-input"
        />
        <input
          v-model="form.email"
          type="email"
          :placeholder="t('contact_email')"
          required
          class="form-input"
        />
        <textarea
          v-model="form.message"
          :placeholder="t('contact_message')"
          required
          rows="5"
          class="form-input form-textarea"
        ></textarea>

        <button type="submit" class="form-btn" :disabled="status === 'sending'">
          <span v-if="status === 'sending'" v-text-id="'contact_sending'"></span>
          <span v-else v-text-id="'contact_send'"></span>
        </button>

        <p v-if="status === 'sent'" class="form-status success" v-text-id="'contact_success'"></p>
        <p v-if="status === 'error'" class="form-status error" v-text-id="'contact_error'"></p>
      </form>
    </div>
  </section>
</template>

<style scoped>
.contact {
  padding: 6rem 2rem 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.contact-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: #fff;
  margin-bottom: 3rem;
  text-align: center;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  max-width: 900px;
  width: 100%;
}

.contact-subtitle {
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 1.5rem;
}

/* ── Redes sociales ── */
.socials-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.social-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 1rem;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.25s ease;
}

.social-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}

.social-link svg {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

/* ── Formulario ── */
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
  font-size: 0.95rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.25s ease, background 0.25s ease;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

.form-input:focus {
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.form-btn {
  align-self: flex-start;
  padding: 0.75rem 2rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.form-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.5);
}

.form-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-status {
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.form-status.success {
  color: #8bdb8b;
}

.form-status.error {
  color: #db8b8b;
}

/* ── Responsive ── */
@media (max-width: 700px) {
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}
</style>
