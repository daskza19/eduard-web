import { watch } from 'vue'
import { useI18n } from '../composables/useI18n.js'

const { currentLang, t } = useI18n()

export const vTextId = {
  mounted(el, binding) {
    const key = binding.value
    el.textContent = t(key)

    const stop = watch(currentLang, () => {
      el.textContent = t(key)
    })

    el._textIdCleanup = stop
  },
  updated(el, binding) {
    const key = binding.value
    el.textContent = t(key)
  },
  unmounted(el) {
    if (el._textIdCleanup) el._textIdCleanup()
  },
}
