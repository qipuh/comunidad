import { ref } from 'vue'

export function useAlert() {
  const alert = ref({
    visible: false,
    type: 'info',
    title: '',
    message: '',
    duration: 4000
  })

  const show = (title, message = '', type = 'info', duration = 4000) => {
    alert.value = {
      visible: true,
      type,
      title,
      message,
      duration
    }
  }

  const success = (title, message = '', duration = 4000) => {
    show(title, message, 'success', duration)
  }

  const error = (title, message = '', duration = 4000) => {
    show(title, message, 'error', duration)
  }

  const warning = (title, message = '', duration = 4000) => {
    show(title, message, 'warning', duration)
  }

  const info = (title, message = '', duration = 4000) => {
    show(title, message, 'info', duration)
  }

  const close = () => {
    alert.value.visible = false
  }

  return {
    alert,
    show,
    success,
    error,
    warning,
    info,
    close
  }
}
